# Evals（designing-character-ips 行為評測）

這些是**行為評測情境**,依 Anthropic 官方「evaluation-driven skill authoring」建議而設:每個
情境描述一段使用者請求(`query`)與**期望行為**(`expected_behavior`),用來檢查這個 skill 是否
在正確時機被觸發、並照 pipeline 產出應有的產物。

與 `tests/` 的差別:`tests/` 是**結構型單元測試**(檔案存在、frontmatter、bundle 完整性),
可離線在 CI 跑;本目錄是**需要一個 agent／模型 harness** 才能實跑的行為評測——CI 只會用
`tests/test_evals.py` 驗證這些情境檔的 schema 是否完整(不呼叫模型)。

## 情境檔格式

`evals/scenarios/*.json`,每檔一個情境:

```json
{
  "name": "quick-mascot-trigger",
  "query": "幫我設計一個吉祥物",
  "should_trigger": true,
  "skills": ["designing-character-ips"],
  "expected_behavior": [
    "先呈現初始化表單(intake),不直接開畫",
    "以壓縮版 pipeline 產出:超級符號 + 三項驗證"
  ],
  "notes": "選填:情境用途說明"
}
```

- `name`(str)、`query`(非空 str)、`expected_behavior`(非空的字串陣列)為必填。
- `should_trigger`(bool,預設 true):正向情境應觸發本 skill,`skills` 需含 `designing-character-ips`;
  負向情境設 `false`、`skills` 設 `[]`,`expected_behavior` 描述「不應套用本 skill」的正確行為。

## 怎麼實跑：`tools/run_evals.py`

模型呼叫本身仍需人工（或你自己接 agent CLI）——這個 repo 刻意不帶任何網路呼叫、API key 或
廠商 SDK。但**除了模型那一步以外的所有環節都已工具化**，所以「跑 evals」是一條指令而不是一段
散文：

```bash
# 1. 看有哪些情境
python3 tools/run_evals.py list

# 2. 產生每個模型 × 每個情境的執行單（含可直接貼的 query 與打勾清單）
python3 tools/run_evals.py pack                       # 預設 haiku / sonnet / opus
python3 tools/run_evals.py pack --models sonnet       # 只跑一個模型

# 3. 照執行單跑完、把結果填進 evals/runs/results-<model>.json 後計分
python3 tools/run_evals.py score evals/runs/results-sonnet.json
```

`pack` 會在 `evals/runs/<model>/<情境名>.md` 產出執行單，並建立一份 `results-<model>.json`
範本（**已存在的 results 檔不會被覆蓋**，所以重跑 pack 不會弄丟你填好的結果）。

`score` 有三種失敗模式，任一發生就以非零狀態結束：

- 該情境在 results 檔裡沒有紀錄（漏跑）
- 觸發結果與 `should_trigger` 不符
- 有 `expected_behavior` 未達成或未記錄

**未達成的項目就是下一輪 SKILL.md／references 的修訂點**——這正是 evals 存在的理由。

`evals/runs/` 已列入 `.gitignore`（產生物）。若要保留某次評測的歷史紀錄，把 results 檔複製到
版控的位置再提交。

以 Haiku／Sonnet／Opus 各跑一次是官方建議：小模型往往需要更明確的指示，Opus 能從精簡指令推出
的東西，Haiku 可能需要寫白。

新增情境時,務必讓 `tests/test_evals.py`（schema）與 `tests/test_run_evals.py`（harness）
仍然通過。
