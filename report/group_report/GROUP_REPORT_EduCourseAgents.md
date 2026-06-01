# Group Report: Lab 3 - Production-Grade Agentic System

- **Team Name**: EduCourseAgents
- **Team ID**: 066
- **Team Members**: Nhi, Huy, Nghĩa
- **Project Topic**: Course Registration Advisor: A ReAct Agent for Educational Course Enrollment
- **Repository**: https://github.com/lemin9802/lab3-066-educourse-react-agent
- **Deployment Date**: 2026-06-01

---

## 1. Executive Summary

Our team built **EduCourse ReAct Agent**, a course registration assistant that helps students find suitable courses, check class availability, validate coupon codes, and calculate final tuition.

The baseline chatbot answers directly without tools. It can give general advice, but it cannot verify course availability, validate coupon codes, or calculate tuition from the course catalog. In contrast, our ReAct Agent v1 follows the **Thought -> Action -> Observation -> Final Answer** pattern and uses tools to ground its answer in fake course data.

The main team scope is **Agent v1**. Agent v2 or deeper improvements are treated as optional individual extensions or future work.

- **Success Rate**: Agent v1 successfully handled the core tested scenarios: Python course tuition calculation, full-class detection, invalid coupon handling, and provider switching.
- **Key Outcome**: The ReAct Agent solved multi-step course registration queries more reliably than the chatbot baseline because it used course tools instead of guessing.

Example user query:

```text
Em muốn học Python beginner vào buổi tối, ngân sách khoảng 1.500.000 VND.
Còn lớp nào phù hợp không và học phí sau mã STUDENT10 là bao nhiêu?
```

Expected ReAct flow:

```text
search_courses -> check_class_slots -> get_coupon -> calculate_tuition -> Final Answer
```

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation

The ReAct Agent v1 uses a loop with the following structure:

```text
User Query
   ↓
Thought: Decide what information is needed
   ↓
Action: Call one tool with JSON arguments
   ↓
Observation: Receive tool result from the system
   ↓
Repeat Thought/Action/Observation if needed
   ↓
Final Answer: Respond to the user
```

For the main successful case, the agent used this sequence:

```text
Thought: Search for Python beginner evening courses.
Action: search_courses({"topic": "Python", "level": "beginner", "schedule": "evening"})
Observation: PY101 found, tuition 1,500,000 VND, slots_left = 5

Thought: Check whether PY101 still has available slots.
Action: check_class_slots({"course_id": "PY101"})
Observation: available = true, slots_left = 5

Thought: Validate the STUDENT10 coupon.
Action: get_coupon({"coupon_code": "STUDENT10"})
Observation: valid = true, discount_percent = 10

Thought: Calculate final tuition.
Action: calculate_tuition({"course_id": "PY101", "coupon_code": "STUDENT10"})
Observation: final_tuition_vnd = 1,350,000

Final Answer: Lớp Python Beginner còn chỗ, học phí sau mã STUDENT10 là 1,350,000 VND.
```

### 2.2 Tool Definitions (Inventory)

| Tool Name | Input Format | Use Case |
| :--- | :--- | :--- |
| `search_courses` | `{"topic": "Python", "level": "beginner", "schedule": "evening"}` | Find courses by topic, level, and optional schedule. |
| `check_class_slots` | `{"course_id": "PY101"}` | Check whether a specific course still has available seats. |
| `get_coupon` | `{"coupon_code": "STUDENT10"}` | Validate a coupon code and return its discount percentage. |
| `calculate_tuition` | `{"course_id": "PY101", "coupon_code": "STUDENT10"}` | Calculate the final tuition after applying a valid coupon. |

### 2.3 Fake Course Catalog

| Course ID | Course Name | Topic | Level | Schedule | Tuition | Slots Left |
| :--- | :--- | :--- | :--- | :--- | ---: | ---: |
| PY101 | Python Beginner | Python | beginner | evening | 1,500,000 VND | 5 |
| PY201 | Python Data Analysis | Python | intermediate | weekend | 2,200,000 VND | 2 |
| WEB101 | Web Development Beginner | Web | beginner | evening | 1,200,000 VND | 0 |
| DS101 | Data Science Foundation | Data Science | beginner | weekend | 2,500,000 VND | 3 |
| AI101 | AI for Beginners | AI | beginner | evening | 1,800,000 VND | 4 |

Coupon catalog:

| Coupon Code | Discount |
| :--- | ---: |
| STUDENT10 | 10% |
| EARLYBIRD | 15% |
| WELCOME5 | 5% |
| NONE | 0% |

### 2.4 LLM Providers Used

- **Primary**: OpenAI `gpt-4o`
- **Secondary (Backup)**: Google Gemini `gemini-2.5-flash`

The same agent can be run with either provider:

```bash
python run_agent.py --provider openai
python run_agent.py --provider gemini
```

This shows that the ReAct loop is separated from the provider implementation.

---

## 3. Telemetry & Performance Dashboard

The system logs structured events during execution. Important events include:

```text
AGENT_START
AGENT_STEP_START
AGENT_LLM_OUTPUT
LLM_METRIC
TOOL_CALL
TOOL_RESULT
AGENT_FINAL_ANSWER
AGENT_END
```

The metrics collected include:

```text
provider
model
prompt_tokens
completion_tokens
total_tokens
latency_ms
cost_estimate
```

### Final Test Run: OpenAI Main Query

Command:

```bash
python run_agent.py --provider openai
```

Query:

```text
Em muốn học Python beginner vào buổi tối, ngân sách khoảng 1.500.000 VND.
Còn lớp nào phù hợp không và học phí sau mã STUDENT10 là bao nhiêu?
```

Observed tool sequence:

```text
search_courses -> check_class_slots -> get_coupon -> calculate_tuition -> Final Answer
```

| Step | Provider | Model | Latency | Total Tokens | Tool / Result |
| ---: | :--- | :--- | ---: | ---: | :--- |
| 1 | OpenAI | gpt-4o | 1758 ms | 497 | `search_courses` |
| 2 | OpenAI | gpt-4o | 1158 ms | 624 | `check_class_slots` |
| 3 | OpenAI | gpt-4o | 904 ms | 697 | `get_coupon` |
| 4 | OpenAI | gpt-4o | 1145 ms | 780 | `calculate_tuition` |
| 5 | OpenAI | gpt-4o | 1399 ms | 908 | `Final Answer` |

- **Average Latency per LLM Step**: approximately 1273 ms
- **Max Latency in Test Run**: 1758 ms
- **Average Tokens per LLM Step**: approximately 701 tokens
- **Summed Tokens Across ReAct Steps**: approximately 3506 tokens
- **Total Cost of Test Suite**: Estimated from logged `cost_estimate`; final exact number depends on the provider pricing formula used in the lab code.

### Provider Switching Test

Command:

```bash
python run_agent.py --provider gemini --query "Em muốn học Web beginner buổi tối. Có lớp nào còn chỗ không?"
```

Result:

```text
The agent searched for Web beginner evening courses and found WEB101.
The tool observation showed slots_left = 0.
The agent correctly answered that the course exists but is full.
```

| Provider | Model | Query | Result |
| :--- | :--- | :--- | :--- |
| OpenAI | gpt-4o | Python beginner + STUDENT10 | Correct final tuition |
| Gemini | gemini-2.5-flash | Web beginner evening | Correctly detected full class |

---

## 4. Root Cause Analysis (RCA) - Failure Traces

### Case Study 1: Language Consistency

- **Input**:

```text
Em muốn học Python beginner buổi tối nhưng dùng mã FAKECODE. Học phí sau giảm là bao nhiêu?
```

- **Observation**: The user asked in Vietnamese, but the agent originally returned the final answer in English.

- **Root Cause**: The system prompt was written mostly in English and did not explicitly require Vietnamese final answers.

- **Fix**: We added explicit rules to the system prompt:

```text
- Always write the Final Answer in Vietnamese.
- If the user asks in Vietnamese, answer in Vietnamese.
```

- **Result**: The agent is expected to return Vietnamese final answers for Vietnamese user queries.

---

### Case Study 2: Full Class Detection

- **Input**:

```text
Em muốn học Web beginner buổi tối. Có lớp nào còn chỗ không?
```

- **Observation**:

```text
Action: search_courses({"topic": "Web", "level": "beginner", "schedule": "evening"})
Observation: WEB101 found, slots_left = 0
Final Answer: The course exists but is full.
```

- **Root Cause**: This was not a failure. It was an important edge case. The course exists but has no available seats.

- **Result**: The agent handled the case correctly by not recommending the class as available.

---

### Case Study 3: Invalid Coupon

- **Input**:

```text
Em muốn học Python beginner buổi tối nhưng dùng mã FAKECODE. Học phí sau giảm là bao nhiêu?
```

- **Observation**:

```text
Action: search_courses({"topic": "Python", "level": "beginner", "schedule": "evening"})
Observation: PY101 found

Action: get_coupon({"coupon_code": "FAKECODE"})
Observation: {"valid": false, "discount_percent": 0, "error": "Coupon code is invalid."}

Final Answer: Coupon is invalid, so no discount is applied.
```

- **Root Cause**: The coupon code did not exist in the coupon catalog.

- **Result**: The agent handled the invalid coupon correctly. The final tuition remained 1,500,000 VND.

---

## 5. Ablation Studies & Experiments

### Experiment 1: Prompt v1 vs Prompt v2

- **Prompt v1**: The agent had a ReAct format prompt but did not explicitly require Vietnamese final answers.
- **Issue**: Some final answers were produced in English even when the user asked in Vietnamese.
- **Prompt v2 Diff**:

```text
Added:
- Always write the Final Answer in Vietnamese.
- If the user asks in Vietnamese, answer in Vietnamese.
```

- **Result**: Improved consistency for Vietnamese demo outputs and final report examples.

### Experiment 2: Chatbot vs Agent

| Case | Chatbot Result | Agent Result | Winner |
| :--- | :--- | :--- | :--- |
| Simple course question | Can answer generally | Can answer using available course tools | Draw / Agent |
| Python beginner + STUDENT10 | May answer generally without verified data | Correctly finds course, checks slots, validates coupon, calculates tuition | **Agent** |
| Web beginner evening | May not verify slot availability | Correctly detects `WEB101` has 0 slots | **Agent** |
| Invalid coupon | May guess or avoid exact validation | Correctly detects invalid coupon and applies no discount | **Agent** |

### Experiment 3: OpenAI vs Gemini Provider Switching

| Provider | Model | Result |
| :--- | :--- | :--- |
| OpenAI | gpt-4o | Successfully completed multi-step tuition calculation |
| Gemini | gemini-2.5-flash | Successfully handled the full-class edge case |

Both providers worked through the same ReAct Agent interface. This confirms that the agent implementation is not tightly coupled to a single LLM provider.

---

## 6. Production Readiness Review

### Security

Current design:

```text
- API keys are stored in .env.
- .env is not committed to GitHub.
- The public repository only includes .env.example.
```

Future production improvements:

```text
- Use a managed secret store instead of local .env files.
- Validate all tool arguments with schemas before execution.
- Add authentication if real student data is used.
```

### Guardrails

Current guardrails:

```text
- max_steps prevents infinite ReAct loops.
- Tool names are restricted to the provided tool list.
- Tool execution errors return structured observations.
- Final answers are forced to Vietnamese for Vietnamese demos.
```

Future guardrails:

```text
- Add retry logic for invalid Action format.
- Add strict JSON schema validation for each tool.
- Add a supervisor layer to review tool calls before execution.
```

### Scaling

Current limitation:

```text
The system uses a small fake course catalog stored in Python dictionaries.
```

Future scaling plan:

```text
- Replace fake dictionary data with a database.
- Add tools for enrollment, prerequisites, schedule conflicts, and payment.
- Cache common course search results.
- Move from a simple loop to a graph-based workflow such as LangGraph for complex branching.
```

### Reliability

Current limitation:

```text
Agent v1 relies on regex-based Action parsing, so it is sensitive to model output format.
```

Future reliability improvements:

```text
- Use structured tool calling instead of regex parsing.
- Add automatic fallback when parsing fails.
- Record pass/fail results for each evaluation case.
- Add more systematic evaluation coverage.
```

---

## Conclusion

The EduCourse ReAct Agent demonstrates that tool-augmented reasoning is more reliable than a normal chatbot for course registration tasks. The chatbot baseline can provide general advice, but the ReAct Agent can ground its answer in course data, coupon validation, and tuition calculation.

The final Agent v1 can:

```text
- Search for courses
- Check class availability
- Validate coupons
- Calculate final tuition
- Switch between OpenAI and Gemini providers
- Produce structured logs and metrics
```

This satisfies the team scope for Lab 3 and provides a foundation for future improvements such as stronger parser guardrails, structured tool calls, and real course database integration.