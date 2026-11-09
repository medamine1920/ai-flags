# AI Feature Flag System – Design Doc

This system decides which AI variant each user gets, measures its quality, and rolls it out or back automatically.

## S0. Requirements & Scope

### F0.1 Functional requirements
(Write at least 8. I'll start you off:)
1. An admin can create a flag with a baseline and an experimental config.
2. An app can ask "which variant for this user?" and always get the same answer for the same user.
3. The system accepts user feedback (👍/👎) on a response and uses it as a quality signal.
4. An admin can restrict a flag to certain request types using request metadata (e.g. only English inputs).
5. An admin can change the rollout %, pause a rollout, and roll back a flag.
6. The system automatically rolls back when quality stays below the threshold.
7. The system compares the quality of the experimental variant against the baseline.
8. The system supports shadow mode (the experimental variant runs, but users only see baseline.)
9. An admin can roll out to specific segments in order (internal → beta → everyone) and allow/block specific user IDs.
10. Every flag change is recorded in an audit log (whom What, When, Why).

11. The system sends a Slack alert on roolback and shows the metrics results on a Dashboard.
12. If quality stays above the threshold, the system automatically advances to the next rollout stage (1% → 5% → 25% → 50% → 100%).
13. The SDK caches the flag config locally. 

### F0.2 Non-functional requirements
(For each one, give a NUMBER and say WHY.)
- evaluate() latency: < 1ms. (The evaluation will runs on every request, Before the AI is called. Every ms it takes is added to every user's wait. It's called the Hot path.)

- Time for a rollback to reach all apps: (A rollback reaches all apps within 30 s, because the SDK refreshes its cached config every 30 s)

- If the flag service is down, the app should: The app keeps working. The SDK uses the last cached config, or serves baseline if it has none. The flag system must never break the host app.

- Max latency track() may add to the user request: < 1 ms.
- Max judge cost per day: 1~2$/day.

6. The app will not block the flux if it's down during a complex request by users.

### F0.3 Estimates
Redo my calculation for YOUR demo: 
pick a request rate 10 req/s

requests/day = requests/sec × 86,400 = 860k request/day
rows/day = requests/day × rows_per_request
rows/day = 860,000
MB/day = 864,000 * 250 ÷ 1,000,000 = 216
GB/month = (MB/day * 30) ÷ 1,000 = 6.48 GB/month
judge_calls/day = 864,000 × 0.05 = 43,3k/day
cost/day = 2$ budget ÷ judge calls/day = 0.0000461894$/day

### F0.4 Out of scope
(At least 4 things you will NOT build, with one line on why.)
8. The app must store the most frequent questions asked before and try to fix the quality of the answer.

11. The admin has permissions to access to beta users contents and history search. (Privacy issue: history is a serious privacy problem. Admins should see aggregated metrics and a sample of outputs, nothing more)

12. The app has an agent who orchestrate the usage tokens per department.(Token budgets per department belong to another project: the “LLM gateway” text that was wrongly pasted into your spec.)



### Open questions
Answered.