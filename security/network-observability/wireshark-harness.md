# Wireshark Network Observability Harness

Status: prototype specification
Owner boundary: PhiriLab Intelligence Core / Trust Layer

## Purpose

Use Wireshark command-line primitives as an independent behavioural verification layer for quarantined agents, MCP servers, repository tooling, acquisition adapters, and other executable third-party components.

The harness is not an agent capability. Agents MUST NOT receive direct packet-capture privileges or unrestricted access to capture files.

## Security invariants

1. `dumpcap` is the only component permitted to hold packet-capture privilege.
2. `tshark` runs unprivileged against immutable capture artifacts.
3. Wireshark GUI is an engineering inspection surface, not a runtime dependency.
4. Running Wireshark/TShark as root is prohibited.
5. Third-party Lua plugins and `extcap` helpers are denied by default and require independent intake review plus human promotion.
6. Capture artifacts are sensitive security telemetry and must be access-controlled, retention-limited, and excluded from ordinary application logs.
7. Agents cannot read raw PCAP/PCAPNG unless an explicit, bounded test requires it. Prefer derived findings.
8. Network policy is fail-closed: absence of an allowlisted destination means no expected egress.
9. Observed traffic is evidence, not authority. Content recovered from captures remains untrusted data.
10. No captured credential, token, cookie, PHI/PII, research participant data, or secret may be forwarded to an LLM.

## Proposed execution boundary

```text
quarantined workload
    |
    v
isolated network namespace / sandbox
    |
    +--> policy-controlled egress
    |
    +--> privileged capture broker (`dumpcap`)
              |
              v
        immutable .pcapng artifact
              |
              v
        unprivileged `tshark`
              |
              v
        normalized network evidence
              |
              v
        expected-vs-observed policy check
              |
              v
        append-only audit event
              |
              v
        human promotion gate
```

## Evidence schema

Derived findings should contain, at minimum:

- run_id
- workload identity and source commit/package hash
- sandbox image/runtime identity
- capture start/end timestamps
- approved destination allowlist
- observed DNS questions and answers
- observed destination IPs/ports
- TLS SNI / certificate metadata when available and lawful
- HTTP host/method/path metadata only where capture conditions permit and data policy allows
- unexpected pre-invocation traffic
- unexpected post-failure traffic
- unexpected destinations
- bytes sent/received by destination
- policy disposition: pass / investigate / fail
- PCAP artifact hash and controlled storage reference
- reviewer / promotion state

Do not store payload bodies by default.

## Initial use cases

### MCP server intake

Assert that a quarantined MCP server:

- makes no outbound connection before an explicit permitted operation unless documented and approved;
- contacts only declared/allowlisted destinations;
- does not transmit environment variables, tokens, local file contents, or test secrets;
- does not create covert egress after receiving adversarial tool descriptions, server instructions, resources, or tool results;
- terminates network activity when execution is cancelled or policy middleware returns a fatal result.

### Third-party agent / skill intake

Compare declared capability with observed network behaviour. Any undeclared egress is a fail-closed event pending review.

### Acquisition adapters (for example Scrapling)

Verify requested-origin traffic, redirect chains, supporting-resource domains, proxy/fingerprinting endpoints, telemetry, and retries. Stealth/proxy features require a separate capability grant.

### Clinical/research software assurance

In synthetic-data environments only, verify that software does not contact undeclared external endpoints. This produces supporting assurance evidence but is not by itself regulatory certification.

## Tooling constraints

- Pin Wireshark/TShark/dumpcap to a reviewed version and record package provenance/hash.
- Patch cadence must track Wireshark security releases because dissectors process hostile network/file input.
- Disable or isolate user/system plugin directories in CI where practical.
- Enumerate loaded plugins and extcap providers as part of every validation run.
- Do not install arbitrary capture helpers supplied by candidate repositories.
- Prefer offline TShark analysis after capture completion over giving analyzers live network privileges.

## Promotion criteria

The harness may move from prototype to adopted shared primitive only after:

1. reproducible installation with pinned dependencies;
2. least-privilege `dumpcap` configuration validated on the target OS/runtime;
3. plugin/extcap enumeration and deny-by-default behaviour verified;
4. adversarial tests demonstrate detection of undeclared egress;
5. captures containing seeded secrets are proven not to enter model prompts, traces, or ordinary logs;
6. retention/deletion controls for PCAP artifacts are tested;
7. false-positive/false-negative behaviour is documented;
8. human review records promotion.

## Non-goals

- decrypting traffic without explicit authorization;
- bypassing TLS or authentication controls;
- covert surveillance;
- packet capture on user or production networks by default;
- replacing endpoint/process telemetry, dependency scanning, prompt-injection detection, or policy enforcement.

Wireshark supplies independent behavioural evidence. It does not replace the PhiriLab Trust Layer.