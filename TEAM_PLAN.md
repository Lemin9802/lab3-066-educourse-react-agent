# Team Plan - Lab 3 EduCourse ReAct Agent

## 1. Project Overview

### Project Topic

**Course Registration Advisor: A ReAct Agent for Educational Course Enrollment**

### Project Idea

Our team will build a ReAct-based educational assistant that helps students choose and register for suitable courses.

The agent can help users:

* Find suitable courses by topic, level, and schedule.
* Check whether a class still has available slots.
* Validate discount coupon codes.
* Calculate the final tuition after discount.
* Compare a normal chatbot baseline with a ReAct Agent v1.

The goal is not to build a full education platform. The goal is to demonstrate how a ReAct Agent performs better than a normal chatbot on multi-step tasks that require tool use and environment feedback.

### Main Team Scope

The required team scope is to build and evaluate **Agent v1**.

Agent v1 should be able to:

```text
Thought -> Action -> Observation -> Thought -> Action -> Observation -> Final Answer
```

Agent v2 or any further improvement is optional. Each member may add small improvements if they have time, but the main team deliverable is Agent v1.

### Example User Query

```text
Em muốn học Python beginner vào buổi tối, ngân sách khoảng 1.500.000 VND.
Còn lớp nào phù hợp không và học phí sau mã STUDENT10 là bao nhiêu?
```

### Expected Agent Behavior

The agent should reason step by step:

```text
Thought -> Action -> Observation -> Thought -> Action -> Observation -> Final Answer
```

Expected flow:

```text
1. Search for Python beginner courses.
2. Check whether the matched course has available slots.
3. Validate the STUDENT10 coupon.
4. Calculate the final tuition.
5. Return a clear final answer in Vietnamese.
```

---

## 2. Repository Information

### Repository

This team works on the forked repository:

```text
https://github.com/lemin9802/lab3-066-educourse-react-agent
```

### Important Repository Rule

We work on the team fork only.

```text
Do not push to the original school repository.
Do not create Pull Requests to the original school repository.
All Pull Requests must target the main branch of the team fork.
```

### Final Report File

The final report will be one file that includes both the group report and the personal reports.

```text
Lab3_066_EduCourseAgents.md
```

The report must include:

```text
1. Public repo link.
2. Commit evidence for each member.
3. Group report.
4. Personal report section for each member.
```

---

## 3. Team Members and Responsibilities

| Member | Role                                                            | Branch                               | Required Commit |
| ------ | --------------------------------------------------------------- | ------------------------------------ | --------------- |
| Nhi    | Lead, ReAct loop, provider switching, integration, final report | `feat/lead-react-provider-switching` | Yes             |
| Huy    | EduCourse tools and course catalog                              | `feat/educourse-tools`               | Yes             |
| Nghĩa  | Chatbot baseline, evaluation, log analysis                      | `feat/evaluation-baseline`           | Yes             |

### Required Commit Rule

Each member must have at least one code commit in the team repository using their own GitHub account.

This is required for personal score.

---

## 4. Project Scope

### In Scope

The project will implement a course registration assistant using a fake course catalog.

The assistant will support:

```text
- Course search
- Class slot checking
- Coupon validation
- Final tuition calculation
- Chatbot vs ReAct Agent v1 comparison
- OpenAI/Gemini provider switching
- Logs and metrics analysis
- Failure analysis for Agent v1
```

### Optional Scope

The following items are optional and can be done by individual members if time allows:

```text
- Agent v2 improvements
- Retry logic
- Better parser guardrails
- Better prompt format
- More test cases
- More detailed metrics
- Prompt ablation experiments
```

### Out of Scope

The project will not implement:

```text
- Real student accounts
- Real payment
- Real school database
- Real enrollment confirmation
- AI tutoring
- Essay grading
- Long-term personalized learning roadmap
- Web UI
```

---

## 5. Fake Data Scope

The project will use a small fake course catalog.

### Example Course Data

```python
COURSES = {
    "PY101": {
        "name": "Python Beginner",
        "topic": "Python",
        "level": "beginner",
        "schedule": "evening",
        "tuition_vnd": 1500000,
        "slots_left": 5
    },
    "PY201": {
        "name": "Python Data Analysis",
        "topic": "Python",
        "level": "intermediate",
        "schedule": "weekend",
        "tuition_vnd": 2200000,
        "slots_left": 2
    },
    "WEB101": {
        "name": "Web Development Beginner",
        "topic": "Web",
        "level": "beginner",
        "schedule": "evening",
        "tuition_vnd": 1200000,
        "slots_left": 0
    },
    "DS101": {
        "name": "Data Science Foundation",
        "topic": "Data Science",
        "level": "beginner",
        "schedule": "weekend",
        "tuition_vnd": 2500000,
        "slots_left": 3
    },
    "AI101": {
        "name": "AI for Beginners",
        "topic": "AI",
        "level": "beginner",
        "schedule": "evening",
        "tuition_vnd": 1800000,
        "slots_left": 4
    }
}
```

### Example Coupon Data

```python
COUPONS = {
    "STUDENT10": 10,
    "EARLYBIRD": 15,
    "WELCOME5": 5,
    "NONE": 0
}
```

---

## 6. Tools to Implement

The ReAct Agent must use tools instead of guessing.

The project will implement four main tools.

---

### Tool 1: `search_courses`

### Purpose

Find courses by topic, level, and optional schedule.

### Input Format

```json
{
  "topic": "Python",
  "level": "beginner",
  "schedule": "evening"
}
```

### Output Example

```json
{
  "matches": [
    {
      "course_id": "PY101",
      "name": "Python Beginner",
      "topic": "Python",
      "level": "beginner",
      "schedule": "evening",
      "tuition_vnd": 1500000,
      "slots_left": 5
    }
  ]
}
```

---

### Tool 2: `check_class_slots`

### Purpose

Check whether a course still has available seats.

### Input Format

```json
{
  "course_id": "PY101"
}
```

### Output Example

```json
{
  "course_id": "PY101",
  "available": true,
  "slots_left": 5
}
```

---

### Tool 3: `get_coupon`

### Purpose

Validate a coupon code and return discount percentage.

### Input Format

```json
{
  "coupon_code": "STUDENT10"
}
```

### Output Example

```json
{
  "valid": true,
  "coupon_code": "STUDENT10",
  "discount_percent": 10
}
```

---

### Tool 4: `calculate_tuition`

### Purpose

Calculate final tuition after applying a coupon.

### Input Format

```json
{
  "course_id": "PY101",
  "coupon_code": "STUDENT10"
}
```

### Output Example

```json
{
  "course_id": "PY101",
  "original_tuition_vnd": 1500000,
  "discount_percent": 10,
  "discount_vnd": 150000,
  "final_tuition_vnd": 1350000
}
```

---

## 7. Branch Strategy

The team will use one branch per member.

```text
main
feat/lead-react-provider-switching
feat/educourse-tools
feat/evaluation-baseline
```

### `main`

Stable branch for final integrated work.

Rules:

```text
- Do not commit directly to main.
- Only merge reviewed Pull Requests into main.
```

### `feat/lead-react-provider-switching`

Owner: Nhi

Purpose:

```text
- Implement ReAct Agent v1 loop.
- Implement Action parser.
- Implement tool execution.
- Add provider switching for OpenAI and Gemini.
- Add run_agent.py.
- Add scripts/compare_providers.py.
- Integrate logs and metrics.
- Prepare final report skeleton.
```

### `feat/educourse-tools`

Owner: Huy

Purpose:

```text
- Implement fake course catalog.
- Implement coupon data.
- Implement EduCourse tools.
- Export TOOLS list with clear descriptions.
```

### `feat/evaluation-baseline`

Owner: Nghĩa

Purpose:

```text
- Implement chatbot baseline.
- Add test cases.
- Add evaluation runner.
- Add log analysis script.
- Prepare comparison table for report.
```

---

## 8. Git Workflow Rules

### Rule 1: Do not commit directly to `main`

Every member must work on their assigned branch.

### Rule 2: Pull before starting work

Before coding, update your local repo.

Command line users:

```bash
git checkout main
git pull origin main
git checkout <your-branch>
```

GitHub Desktop users:

```text
Current Branch: main
Fetch origin
Pull origin
Switch back to your branch
```

### Rule 3: Commit with clear messages

Good commit messages:

```text
Add EduCourse tools and course catalog
Implement ReAct action parser
Add chatbot baseline and test cases
Add provider switching for OpenAI and Gemini
Add evaluation log analyzer
```

Bad commit messages:

```text
update
fix
final
abc
test
```

### Rule 4: Push branch and create Pull Request

After finishing a task:

```text
1. Commit changes.
2. Push branch.
3. Create Pull Request into main of the team fork.
4. Wait for lead review.
```

### Rule 5: Pull Request target must be team fork

Correct PR target:

```text
base repository: lemin9802/lab3-066-educourse-react-agent
base branch: main
compare branch: feat/...
```

Wrong PR target:

```text
base repository: original school repository
```

Do not create PRs to the school repository.

---

## 9. Security Rules

Never commit:

```text
.env
API keys
logs/
models/
__pycache__/
*.log
.DS_Store
.venv/
```

The `.env` file is local only.

Use `.env.example` as the shared template.

Allowed to commit:

```text
.env.example
requirements.txt
README.md
source code
test cases
report files
TEAM_PLAN.md
```

### API Key Rule

API keys must stay local.

Do not paste API keys into:

```text
- GitHub
- Pull Requests
- Issues
- README
- Report
- Team chat
- Source code
```

---

## 10. Individual Task Details

## Lead Tasks

Owner: Nhi

Branch:

```text
feat/lead-react-provider-switching
```

### Main Responsibilities

```text
1. Implement ReActAgent.run() for Agent v1.
2. Implement Final Answer detection.
3. Implement Action parser.
4. Implement dynamic tool execution.
5. Add max_steps guardrail.
6. Feed Observation back into the next prompt.
7. Add provider_factory.py.
8. Support OpenAI/Gemini switching.
9. Add run_agent.py with CLI arguments.
10. Add scripts/compare_providers.py.
11. Review PRs from Huy and Nghĩa.
12. Integrate final demo.
13. Prepare final report.
```

### Files

```text
src/agent/agent.py
src/core/provider_factory.py
run_agent.py
scripts/compare_providers.py
report/Lab3_066_EduCourseAgents.md
TEAM_PLAN.md
```

### Done When

```text
python run_agent.py --provider openai
python run_agent.py --provider gemini
```

Both commands should run successfully and return a Final Answer.

Optional improvement if time allows:

```text
- Improve parser robustness.
- Add retry logic.
- Add clearer error messages.
- Add prompt v2 experiment.
```

---

## Member 2 Tasks

Owner: Huy

Branch:

```text
feat/educourse-tools
```

### Main Responsibilities

```text
1. Create src/tools/educourse_tools.py.
2. Add COURSES fake data.
3. Add COUPONS fake data.
4. Implement search_courses().
5. Implement check_class_slots().
6. Implement get_coupon().
7. Implement calculate_tuition().
8. Export TOOLS list.
9. Write clear tool descriptions.
```

### Files

```text
src/tools/educourse_tools.py
```

### Done When

```text
- run_agent.py can import TOOLS from src.tools.educourse_tools.
- Each tool returns a dictionary.
- Tool descriptions are specific enough for the ReAct Agent.
- At least four tools are implemented.
```

Optional improvement if time allows:

```text
- Add schedule filtering.
- Add budget checking helper.
- Add better error output for unknown course_id or invalid coupon.
```

---

## Member 3 Tasks

Owner: Nghĩa

Branch:

```text
feat/evaluation-baseline
```

### Main Responsibilities

```text
1. Create chatbot baseline.
2. Create test cases.
3. Create evaluation runner.
4. Create log analyzer.
5. Compare Chatbot vs Agent v1.
6. Summarize success rate, latency, token count, loop count, and failure types.
```

### Files

```text
src/chatbot_baseline.py
evaluation/test_cases.py
evaluation/run_evaluation.py
evaluation/analyze_logs.py
```

### Done When

```text
- At least 6 test cases exist.
- Evaluation script can run multiple cases.
- Results can be converted into a report table.
- At least one successful trace and one failed trace are documented.
```

Optional improvement if time allows:

```text
- Add Agent v1 vs optional improved version comparison.
- Add more test cases.
- Add CSV or Markdown output for evaluation results.
```

---

## 11. Test Cases

The evaluation should include at least 6 test cases.

```python
TEST_CASES = [
    {
        "id": "simple_001",
        "query": "Trung tâm có những khóa học nào?",
        "expected": "List available courses"
    },
    {
        "id": "course_001",
        "query": "Em muốn học Python beginner buổi tối, dùng mã STUDENT10. Học phí cuối cùng là bao nhiêu?",
        "expected": "Find PY101, check slots, apply coupon, calculate tuition"
    },
    {
        "id": "course_002",
        "query": "Em muốn học Web beginner buổi tối. Có lớp nào còn chỗ không?",
        "expected": "Detect WEB101 has zero slots"
    },
    {
        "id": "course_003",
        "query": "Em muốn học Data Science beginner cuối tuần, ngân sách 2.000.000 VND. Có phù hợp không?",
        "expected": "Find DS101 but detect tuition exceeds budget"
    },
    {
        "id": "course_004",
        "query": "Em muốn học AI beginner buổi tối, dùng mã EARLYBIRD. Tính học phí sau giảm.",
        "expected": "Find AI101, apply 15 percent discount"
    },
    {
        "id": "failure_001",
        "query": "Em muốn học Python nâng cao nhưng dùng mã FAKECODE. Có giảm giá không?",
        "expected": "Handle invalid coupon"
    }
]
```

---

## 12. Agent v1 and Optional Improvements Plan

### Agent v1

Agent v1 is the required team deliverable.

Expected capabilities:

```text
- Call tools.
- Parse Action.
- Return Observation.
- Feed Observation back into the next prompt.
- Produce Final Answer.
- Stop after max_steps if no Final Answer is produced.
```

Possible Agent v1 issues:

```text
- Recommends a full course with slots_left = 0.
- Fails to parse Action if model returns markdown.
- Calls a hallucinated tool.
- Loops until max_steps.
- Ignores invalid coupon result.
```

### Optional Improvements

Further improvements are optional and can be done by any member if time allows.

Possible optional improvements:

```text
- Add stricter system prompt.
- Require check_class_slots before recommending any course.
- Improve Action parser.
- Strip markdown fences from model output.
- Add better tool error messages.
- Add max_steps fallback.
- Add clearer tool descriptions.
- Add a small Agent v1 vs improved-agent comparison.
```

### Example Failure Case for Report

Input:

```text
Em muốn học Web beginner buổi tối. Có lớp nào còn chỗ không?
```

Possible Agent v1 issue:

```text
Agent recommends WEB101 even though slots_left = 0.
```

Root cause:

```text
Agent did not check class availability before recommending the course.
```

Possible optional fix:

```text
System prompt updated:
Before recommending any course, always call check_class_slots.
If slots_left is 0, do not recommend the course as available.
```

Expected improved answer:

```text
Lớp Web Development Beginner hiện đã hết chỗ. Bạn chưa thể đăng ký lớp này.
Bạn có thể chọn lớp khác còn slot hoặc quay lại sau khi có lịch mở thêm.
```

---

## 13. Provider Switching Plan

The project should support both OpenAI and Gemini.

The agent should be runnable with:

```bash
python run_agent.py --provider openai
python run_agent.py --provider gemini
```

### Expected Providers

```text
OpenAI: primary provider for final demo
Gemini: secondary provider for provider switching comparison
```

### Provider Switching Goal

The same ReAct Agent should run with both providers through the shared provider interface.

The report should compare:

```text
- Whether both providers returned a usable Final Answer.
- Latency difference.
- Token usage difference if available.
- Formatting differences that affected Action parsing.
```

---

## 14. Logs and Metrics Plan

The team will use structured logs to analyze the agent.

Metrics to capture:

```text
- Success rate
- Latency
- Token count
- Loop count
- Parser errors
- Hallucinated tool errors
- Timeout / max_steps errors
- Tool errors
```

Important log events:

```text
AGENT_START
AGENT_STEP_START
AGENT_LLM_OUTPUT
LLM_METRIC
TOOL_CALL
TOOL_RESULT
AGENT_PARSE_ERROR
AGENT_FINAL_ANSWER
AGENT_END
```

The report should include:

```text
1. One successful trace from Agent v1.
2. One failed trace or limitation from Agent v1.
3. Root Cause Analysis.
4. Optional improvement discussion if any member implements it.
```

---

## 15. Final Deliverables

### Code

```text
- ReAct Agent v1 implementation
- EduCourse tools
- Chatbot baseline
- Evaluation scripts
- Provider switching runner
- Log analyzer
```

### Report

Final report file:

```text
Lab3_066_EduCourseAgents.md
```

The report must include:

```text
- Submission information
- Public repo link
- Commit evidence table
- Group report
- Personal report for each member
- Tool inventory
- ReAct flowchart
- Successful trace
- Failed trace or limitation trace
- Metrics table
- Chatbot vs Agent v1 comparison
- Optional improvements if implemented
- Future improvements
```

### Commit Evidence Table

The final report should include:

```md
| Member | Role | Branch | Commit Link |
|---|---|---|---|
| Nhi | Lead, ReAct loop, provider switching | feat/lead-react-provider-switching | [link] |
| Huy | EduCourse tools and catalog | feat/educourse-tools | [link] |
| Nghĩa | Baseline and evaluation | feat/evaluation-baseline | [link] |
```

---

## 16. Progress Checklist

## Repository

```text
[ ] Fork repository confirmed.
[ ] Team fork is public.
[ ] Team fork link added to this file.
[ ] Original school repository is not used for PRs.
[ ] Members invited to the team fork.
```

## Branches

```text
[ ] Nhi branch created.
[ ] Huy branch created.
[ ] Nghĩa branch created.
```

## Nhi

```text
[ ] ReActAgent.run() implemented for Agent v1.
[ ] Action parser implemented.
[ ] Tool execution implemented.
[ ] Provider factory implemented.
[ ] run_agent.py implemented.
[ ] OpenAI run tested.
[ ] Gemini run tested.
[ ] Final demo prepared.
[ ] Lead personal report completed.
[ ] Optional improvements documented if implemented.
```

## Huy

```text
[ ] Course catalog implemented.
[ ] Coupon catalog implemented.
[ ] search_courses implemented.
[ ] check_class_slots implemented.
[ ] get_coupon implemented.
[ ] calculate_tuition implemented.
[ ] TOOLS list exported.
[ ] Member 2 personal report completed.
[ ] Optional improvements documented if implemented.
```

## Nghĩa

```text
[ ] Chatbot baseline implemented.
[ ] Test cases implemented.
[ ] Evaluation runner implemented.
[ ] Log analyzer implemented.
[ ] Metrics table prepared.
[ ] Member 3 personal report completed.
[ ] Optional improvements documented if implemented.
```

## Final Report

```text
[ ] Public repo link included.
[ ] Commit evidence included.
[ ] Group report completed.
[ ] All personal reports included.
[ ] Tool inventory included.
[ ] Flowchart included.
[ ] Successful trace included.
[ ] Failed trace or limitation trace included.
[ ] Metrics table included.
[ ] Chatbot vs Agent v1 comparison included.
[ ] Optional improvements included if implemented.
[ ] File renamed to Lab3_066_EduCourseAgents.md.
```

---

## 17. Team Communication Template

Use this message in the team chat:

```text
Team mình chốt đề tài Lab 3 là Course Registration Advisor.

Mình đã fork repo mẫu của trường và team mình sẽ làm trên fork này, không đóng góp ngược về repo gốc của trường.

Repo nộp bài:
https://github.com/lemin9802/lab3-066-educourse-react-agent

Scope chính:
Team mình làm đến Agent v1. Agent v1 cần chạy được vòng Thought -> Action -> Observation -> Final Answer, gọi được tools, có chatbot baseline, logs và evaluation.
Agent v2 hoặc các improvement sâu hơn là optional, ai có thời gian thì làm thêm và ghi vào personal report.

Workflow:
- Không commit trực tiếp vào main.
- Mỗi người làm branch riêng.
- Code xong thì push branch và tạo Pull Request vào main của repo fork này.
- Không tạo PR về repo gốc của trường.
- Không commit .env, API key, logs, models, __pycache__, .venv.
- Mỗi người phải có ít nhất 1 code commit bằng GitHub account của mình để được personal score.

Branch:
- Nhi: feat/lead-react-provider-switching
  Việc: ReAct loop v1, parser, tool execution, OpenAI/Gemini provider switching, runner, report integration.

- Huy: feat/educourse-tools
  Việc: course catalog + tools: search_courses, check_class_slots, get_coupon, calculate_tuition.

- Nghĩa: feat/evaluation-baseline
  Việc: chatbot baseline + test cases + evaluation/log analysis.

Report file dự kiến:
Lab3_066_EduCourseAgents.md
```

---

## 18. Definition of Done

The project is considered done when:

```text
1. The public fork repository contains the final code.
2. Each member has at least one code commit.
3. The ReAct Agent v1 can solve at least one multi-step course registration query.
4. The chatbot baseline and Agent v1 are compared.
5. Logs and metrics are used in the report.
6. At least one successful Agent v1 trace is documented.
7. At least one failed trace or limitation is documented and analyzed.
8. OpenAI/Gemini provider switching is demonstrated.
9. The final report includes both group and personal sections.
10. Optional Agent v2 or improvements are documented only if implemented.
11. The final report filename follows the required Lab3_066_EduCourseAgents.md format.
```
