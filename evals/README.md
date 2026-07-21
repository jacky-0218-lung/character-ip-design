# Evals（character-ip-design 行為評測）

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
  "skills": ["character-ip-design"],
  "expected_behavior": [
    "先呈現初始化表單(intake),不直接開畫",
    "以壓縮版 pipeline 產出:超級符號 + 三項驗證"
  ],
  "notes": "選填:情境用途說明"
}
```

- `name`(str)、`query`(非空 str)、`expected_behavior`(非空的字串陣列)為必填。
- `should_trigger`(bool,預設 true):正向情境應觸發本 skill,`skills` 需含 `character-ip-design`;
  負向情境設 `false`、`skills` 設 `[]`,`expected_behavior` 描述「不應套用本 skill」的正確行為。

## 怎麼實跑(需外部 harness)

1. 讀取每個情境檔,把 `query` 交給掛載了本 skill 的 agent(Claude/Codex 皆可)。
2. 檢查:是否觸發本 skill(對照 `should_trigger`);產出是否覆蓋每一條 `expected_behavior`。
3. 以 Haiku／Sonnet／Opus 各跑一次——官方建議小模型可能需要更明確的指示。
4. 把 gap 回饋成下一輪 SKILL.md／references 的修訂點。

新增情境時,務必讓 `tests/test_evals.py` 仍然通過(schema 驗證)。
