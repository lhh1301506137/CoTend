#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";

const SCHEMA = "cotend.semantic-contract.v1";
const LEVELS = new Set(["L0", "L1", "L2"]);
const SCOPES = new Set(["current_mvp", "active_path", "target_feature", "full_project"]);
const TOP_LEVEL_KEYS = new Set([
  "schema",
  "contract_id",
  "node_id",
  "semantic_level",
  "parent_node_id",
  "scope",
  "meaning",
  "protected_product_rules",
]);
const DIGEST_PATTERN = /^sha256:[0-9a-f]{64}$/;

function fail(message) {
  const error = new Error(message);
  error.name = "SemanticContractError";
  throw error;
}

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function normalizeString(value) {
  return value.replace(/\r\n?/g, "\n").normalize("NFC");
}

function skipWhitespace(source, start) {
  let index = start;
  while (index < source.length && /[\u0009\u000a\u000d\u0020]/.test(source[index])) index += 1;
  return index;
}

function scanJsonString(source, start, path) {
  if (source[start] !== '"') fail(`expected JSON string at ${path}`);
  let index = start + 1;
  while (index < source.length) {
    if (source[index] === "\\") {
      index += 2;
      continue;
    }
    if (source[index] === '"') {
      const end = index + 1;
      try {
        return { value: JSON.parse(source.slice(start, end)), end };
      } catch (error) {
        fail(`invalid JSON string at ${path}: ${error.message}`);
      }
    }
    index += 1;
  }
  fail(`unterminated JSON string at ${path}`);
}

function scanJsonValue(source, start, path) {
  let index = skipWhitespace(source, start);
  const token = source[index];

  if (token === "{") {
    index = skipWhitespace(source, index + 1);
    const keys = new Set();
    if (source[index] === "}") return index + 1;
    while (index < source.length) {
      const parsedKey = scanJsonString(source, index, `${path}.<key>`);
      const normalizedKey = normalizeString(parsedKey.value);
      if (keys.has(normalizedKey)) {
        fail(`duplicate or normalization-ambiguous JSON key at ${path}: ${normalizedKey}`);
      }
      keys.add(normalizedKey);
      index = skipWhitespace(source, parsedKey.end);
      if (source[index] !== ":") fail(`expected ':' after JSON key at ${path}`);
      index = scanJsonValue(source, index + 1, `${path}.${normalizedKey}`);
      index = skipWhitespace(source, index);
      if (source[index] === "}") return index + 1;
      if (source[index] !== ",") fail(`expected ',' or '}' at ${path}`);
      index = skipWhitespace(source, index + 1);
    }
    fail(`unterminated JSON object at ${path}`);
  }

  if (token === "[") {
    index = skipWhitespace(source, index + 1);
    if (source[index] === "]") return index + 1;
    let itemIndex = 0;
    while (index < source.length) {
      index = scanJsonValue(source, index, `${path}[${itemIndex}]`);
      index = skipWhitespace(source, index);
      if (source[index] === "]") return index + 1;
      if (source[index] !== ",") fail(`expected ',' or ']' at ${path}`);
      index = skipWhitespace(source, index + 1);
      itemIndex += 1;
    }
    fail(`unterminated JSON array at ${path}`);
  }

  if (token === '"') return scanJsonString(source, index, path).end;

  const primitive = /^(?:true|false|null|-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)/.exec(
    source.slice(index),
  );
  if (!primitive) fail(`invalid JSON value at ${path}`);
  return index + primitive[0].length;
}

function assertUnambiguousJson(source, label) {
  const withoutBom = source.replace(/^\uFEFF/, "");
  const end = skipWhitespace(withoutBom, scanJsonValue(withoutBom, 0, "$"));
  if (end !== withoutBom.length) fail(`${label} has trailing or ambiguous JSON input`);
  return withoutBom;
}

const DIGEST_METADATA_QUALIFIERS = new Set([
  "actual",
  "binding",
  "canonical",
  "computed",
  "confirmation",
  "content",
  "contract",
  "current",
  "expected",
  "payload",
  "protected",
  "semantic",
  "source",
  "stored",
  "target",
  "verification",
]);

function isSelfReferentialDigestKey(key) {
  const normalized = normalizeString(key)
    .replace(/([a-z0-9])([A-Z])/g, "$1_$2")
    .replace(/[^A-Za-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .toLowerCase();
  const match = /^(?:(.+)_)?(?:digest|hash|sha_?256)$/.exec(normalized);
  if (!match) return false;
  if (!match[1]) return true;
  return match[1].split("_").every((token) => DIGEST_METADATA_QUALIFIERS.has(token));
}

function rejectSelfReference(value, path = "$") {
  if (Array.isArray(value)) {
    value.forEach((item, index) => rejectSelfReference(item, `${path}[${index}]`));
    return;
  }
  if (!isPlainObject(value)) return;

  for (const [key, child] of Object.entries(value)) {
    if (isSelfReferentialDigestKey(key)) {
      fail(`self-referential hash field is forbidden at ${path}.${key}`);
    }
    rejectSelfReference(child, `${path}.${key}`);
  }
}

function validateProtectedContent(value, path) {
  if (typeof value === "string") {
    if (normalizeString(value).trim() === "") fail(`protected text must be non-empty at ${path}`);
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => validateProtectedContent(item, `${path}[${index}]`));
    return;
  }
  if (isPlainObject(value)) {
    if (Object.keys(value).length === 0) fail(`protected object must be non-empty at ${path}`);
    for (const [key, child] of Object.entries(value)) {
      if (normalizeString(key).trim() === "") fail(`protected object key must be non-empty at ${path}`);
      validateProtectedContent(child, `${path}.${key}`);
    }
    return;
  }
  fail(`protected content must use strings, arrays, or objects at ${path}`);
}

function validatePayload(payload) {
  if (!isPlainObject(payload)) fail("payload must be one JSON object");
  rejectSelfReference(payload);

  for (const key of Object.keys(payload)) {
    if (!TOP_LEVEL_KEYS.has(key)) fail(`unknown top-level payload field: ${key}`);
  }
  for (const key of TOP_LEVEL_KEYS) {
    if (!Object.prototype.hasOwnProperty.call(payload, key)) fail(`missing required payload field: ${key}`);
  }

  if (payload.schema !== SCHEMA) fail(`schema must be ${SCHEMA}`);
  if (typeof payload.contract_id !== "string" || !/^SC-[A-Za-z0-9][A-Za-z0-9._:-]*$/.test(payload.contract_id)) {
    fail("contract_id must be a non-empty stable ID beginning with SC-");
  }
  if (typeof payload.node_id !== "string" || normalizeString(payload.node_id).trim() === "") {
    fail("node_id must be a non-empty string");
  }
  if (!LEVELS.has(payload.semantic_level)) fail("semantic_level must be L0, L1, or L2");
  if (!SCOPES.has(payload.scope)) fail("scope is not a supported protected scope");

  if (payload.semantic_level === "L0") {
    if (payload.parent_node_id !== null) fail("L0 parent_node_id must be null");
  } else if (typeof payload.parent_node_id !== "string" || normalizeString(payload.parent_node_id).trim() === "") {
    fail("L1/L2 parent_node_id must be a non-empty string");
  }

  if (!isPlainObject(payload.meaning) || Object.keys(payload.meaning).length === 0) {
    fail("meaning must be a non-empty object");
  }
  validateProtectedContent(payload.meaning, "$.meaning");
  if (!Array.isArray(payload.protected_product_rules)) {
    fail("protected_product_rules must be an array");
  }
  payload.protected_product_rules.forEach((rule, index) => {
    if (typeof rule !== "string" || normalizeString(rule).trim() === "") {
      fail(`protected_product_rules[${index}] must be a non-empty string`);
    }
  });

  return payload;
}

function canonicalJson(value, path = "$") {
  if (value === null || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "string") return JSON.stringify(normalizeString(value));
  if (typeof value === "number") {
    if (!Number.isFinite(value)) fail(`non-finite number at ${path}`);
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((item, index) => canonicalJson(item, `${path}[${index}]`)).join(",")}]`;
  }
  if (!isPlainObject(value)) fail(`unsupported JSON value at ${path}`);

  const normalizedEntries = Object.entries(value).map(([key, child]) => [
    normalizeString(key),
    child,
    key,
  ]);
  normalizedEntries.sort(([left], [right]) => (left < right ? -1 : left > right ? 1 : 0));

  const serialized = [];
  let previousKey;
  for (const [normalizedKey, child, originalKey] of normalizedEntries) {
    if (previousKey === normalizedKey) {
      fail(`ambiguous keys normalize to the same value at ${path}: ${originalKey}`);
    }
    previousKey = normalizedKey;
    serialized.push(`${JSON.stringify(normalizedKey)}:${canonicalJson(child, `${path}.${normalizedKey}`)}`);
  }
  return `{${serialized.join(",")}}`;
}

function digestPayload(payload) {
  validatePayload(payload);
  const canonicalJsonText = canonicalJson(payload);
  const digest = `sha256:${createHash("sha256").update(canonicalJsonText, "utf8").digest("hex")}`;
  return { canonicalJson: canonicalJsonText, digest };
}

function parseJson(source, label) {
  const unambiguous = assertUnambiguousJson(source, label);
  try {
    return JSON.parse(unambiguous);
  } catch (error) {
    fail(`${label} is not valid JSON: ${error.message}`);
  }
}

function declaredContractIds(source) {
  const ids = [];
  const pattern = /("(?:\\.|[^"\\])*")[\u0009\u000a\u000d\u0020]*:[\u0009\u000a\u000d\u0020]*("(?:\\.|[^"\\])*")/g;
  let match;
  while ((match = pattern.exec(source)) !== null) {
    try {
      const key = JSON.parse(match[1]);
      const value = JSON.parse(match[2]);
      if (normalizeString(key) === "contract_id" && typeof value === "string") {
        ids.push(normalizeString(value));
      }
    } catch {
      // The strict parser reports malformed input. This scan only scopes target-ID ambiguity.
    }
  }
  return ids;
}

function extractContractBodies(markdown) {
  const bodies = [];
  const fencePattern = /^```([^\r\n]*)\r?\n([\s\S]*?)^```[ \t]*$/gm;
  let match;
  while ((match = fencePattern.exec(markdown)) !== null) {
    if (!match[1].split(/\s+/).includes(SCHEMA)) continue;
    bodies.push(match[2]);
  }
  return bodies;
}

function extractContractPayloads(markdown) {
  return extractContractBodies(markdown).map((body, index) => {
    const payload = parseJson(body, `${SCHEMA} fenced payload #${index + 1}`);
    validatePayload(payload);
    return payload;
  });
}

function extractDecisionSection(markdown, decisionRef) {
  const normalized = markdown.replace(/\r\n?/g, "\n");
  const lines = normalized.split("\n");
  const headings = [];
  for (let index = 0; index < lines.length; index += 1) {
    const match = /^##[ \t]+(DEC-[A-Za-z0-9._-]+)(?:[ \t]*[:：]|[ \t]+|$)/.exec(lines[index]);
    if (match) headings.push({ id: match[1], index });
  }
  const matches = headings.filter(({ id }) => id === decisionRef);
  if (matches.length !== 1) fail(`decision_ref must resolve to exactly one entry: ${decisionRef}`);
  const start = matches[0].index;
  const next = headings.find(({ index }) => index > start);
  return lines.slice(start, next ? next.index : lines.length).join("\n");
}

function parseArguments(argv) {
  const [command, ...rest] = argv;
  if (!new Set(["digest", "verify", "verify-log"]).has(command)) {
    fail("usage: semantic-contract.mjs <digest|verify|verify-log> [--input path] [--expected sha256:...] [--contract-id ID] [--decision-ref DEC-ID]");
  }

  const options = { command };
  const seen = new Set();
  for (let index = 0; index < rest.length; index += 1) {
    const token = rest[index];
    if (!new Set(["--input", "--expected", "--contract-id", "--decision-ref"]).has(token)) fail(`unknown argument: ${token}`);
    if (seen.has(token)) fail(`duplicate argument: ${token}`);
    seen.add(token);
    const value = rest[index + 1];
    if (value === undefined || value.startsWith("--")) fail(`missing value for ${token}`);
    options[token.slice(2).replace("-", "_")] = value;
    index += 1;
  }

  const allowed = {
    digest: new Set(["input"]),
    verify: new Set(["input", "expected"]),
    "verify-log": new Set(["input", "expected", "contract_id", "decision_ref"]),
  }[command];
  for (const key of Object.keys(options)) {
    if (key !== "command" && !allowed.has(key)) fail(`argument is not valid for ${command}: --${key.replace("_", "-")}`);
  }
  return options;
}

async function readInput(path) {
  if (path) return readFile(path, "utf8");
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  if (chunks.length === 0) fail("no input supplied; use --input or stdin");
  return Buffer.concat(chunks).toString("utf8");
}

function requireExpected(expected) {
  if (typeof expected !== "string" || !DIGEST_PATTERN.test(expected)) {
    fail("--expected must be sha256 followed by 64 lowercase hex characters");
  }
}

async function main() {
  const options = parseArguments(process.argv.slice(2));
  const source = await readInput(options.input);

  if (options.command === "digest" || options.command === "verify") {
    const payload = parseJson(source, "input");
    const { canonicalJson, digest } = digestPayload(payload);
    if (options.command === "verify") {
      requireExpected(options.expected);
      if (digest !== options.expected) fail(`digest mismatch: expected ${options.expected}, computed ${digest}`);
    }
    process.stdout.write(`${JSON.stringify({
      schema: SCHEMA,
      contract_id: normalizeString(payload.contract_id),
      digest,
      verified: options.command === "verify",
      canonical_json: canonicalJson,
    })}\n`);
    return;
  }

  if (typeof options.contract_id !== "string" || options.contract_id.trim() === "") {
    fail("verify-log requires --contract-id");
  }
  if (typeof options.decision_ref !== "string" || !/^DEC-[A-Za-z0-9._-]+$/.test(options.decision_ref)) {
    fail("verify-log requires --decision-ref with one DEC-* entry ID");
  }
  requireExpected(options.expected);

  const decisionSection = extractDecisionSection(source, options.decision_ref);
  const payloads = extractContractPayloads(decisionSection);
  if (payloads.length === 0) fail(`no ${SCHEMA} fenced payloads found in ${options.decision_ref}`);

  const targetId = normalizeString(options.contract_id);
  const sectionMatches = payloads.filter((payload) => normalizeString(payload.contract_id) === targetId);
  if (sectionMatches.length !== 1) {
    fail(`contract_id must match exactly one payload in ${options.decision_ref}: ${options.contract_id}`);
  }

  let globalMatches = 0;
  for (const body of extractContractBodies(source)) {
    let candidate;
    try {
      candidate = parseJson(body, `${SCHEMA} candidate payload`);
    } catch {
      if (declaredContractIds(body).includes(targetId)) {
        fail(`target contract_id appears in an invalid or ambiguous payload: ${options.contract_id}`);
      }
      // Malformed payloads for unrelated IDs do not widen this node's block.
      continue;
    }

    const candidateId = typeof candidate.contract_id === "string" ? normalizeString(candidate.contract_id) : null;
    if (candidateId === targetId) {
      try {
        validatePayload(candidate);
      } catch {
        fail(`target contract_id appears in an invalid or ambiguous payload: ${options.contract_id}`);
      }
      globalMatches += 1;
    }
  }
  if (globalMatches !== 1) fail(`duplicate contract_id in decision log: ${options.contract_id}`);

  const target = sectionMatches[0];
  const { canonicalJson, digest } = digestPayload(target);
  if (digest !== options.expected) fail(`digest mismatch: expected ${options.expected}, computed ${digest}`);

  process.stdout.write(`${JSON.stringify({
    schema: SCHEMA,
    contract_id: normalizeString(target.contract_id),
    decision_ref: options.decision_ref,
    digest,
    verified: true,
    payload_count: payloads.length,
    canonical_json: canonicalJson,
  })}\n`);
}

main().catch((error) => {
  process.stderr.write(`${JSON.stringify({ error: error.message, type: error.name })}\n`);
  process.exitCode = 2;
});
