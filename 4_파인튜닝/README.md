# 4_파인튜닝 — 내 모델 만들기

내가 모은 데이터로 작은 AI 모델(Qwen2.5-3B)에게 **MBC 기사 말투**를 가르치고,
원본 모델 · GPT와 누가 더 잘 쓰는지 비교해요.

> **용어 정리**
> - **Studio** = Unsloth Studio. 브라우저에서 `127.0.0.1:8888`로 여는 학습 프로그램. **버튼을 눌러** 학습해요.
> - **Jupyter 노트북** = VS Code에서 여는 `.ipynb` 파일. **코드 칸을 실행해서** 학습해요.
> - 둘 중 **하나만** 쓰면 돼요. 결과는 같아요.

---

## 한눈에 보는 순서

```
① 데이터 나누기 → ② 학습 → ③ 내보내기(GGUF) → ④ Ollama 준비 → ⑤ 내 모델 등록 → ⑥ 비교 → ⑦ 날씨로 톤 시험
```

| 단계 | 어디서 | 만들어지는 것 |
|---|---|---|
| ① 데이터 나누기 | Jupyter 노트북 `1_split_data.ipynb` | `train.jsonl` `eval.jsonl` `test.jsonl` |
| ② 학습 | Studio **또는** Jupyter 노트북 `2_train_unsloth_gpu.ipynb` | 학습한 모델 (`lead_model` 폴더) |
| ③ 내보내기 | Studio의 Export 버튼 **또는** Jupyter 노트북 「5. GGUF」 칸 | `lead_model_gguf` 폴더 |
| ④ Ollama 준비 | 터미널 | 원본 모델 `qwen2.5:3b` |
| ⑤ 내 모델 등록 | 터미널 | 내 모델 `mbcsports` |
| ⑥ 비교 | Jupyter 노트북 `4_compare_results.ipynb` | `answers.jsonl` `compare_report.html` |
| ⑦ 날씨로 톤 시험 | Jupyter 노트북 `5_weather_tone_test.ipynb` | `weather_report.html` `meteo_report.html` |

> 터미널 여는 법: VS Code에서 `Ctrl` + `` ` `` (숫자 1 왼쪽 키)

---

## ④ Ollama 준비 — 명령 한 줄

**1.** 터미널에 아래 두 줄을 입력해요.

```powershell
cd 4_파인튜닝
powershell -ExecutionPolicy Bypass -File .\setup_ollama.ps1
```

**2.** 계정 만들기 창이 뜨면 → **로그인하지 말고** `No thanks, I'll use Ollama locally` 클릭

**3.** 마지막에 이렇게 나오면 성공 ✅

```
qwen2.5:3b    357c53fb659c    1.9 GB
준비 끝! 이제 1_split_data.ipynb의 비교 칸을 실행하세요.
```

> 💡 이미 설치돼 있으면 알아서 건너뛰어요. 여러 번 실행해도 괜찮아요.

---

## ⑤ 내 모델 등록 — 3단계

③에서 내보내면 이런 폴더가 생겨요.

```
4_파인튜닝
└─ lead_model_gguf
   ├─ Modelfile                         ← Ollama에게 주는 설명서
   └─ Qwen2.5-3B-Instruct.Q4_K_M.gguf   ← 내 모델 파일 (약 2GB)
```

**1. Modelfile 첫 줄 확인하기**

VS Code에서 `Modelfile`을 클릭해서 열어요. **첫 줄**이 아래처럼 GGUF 파일 이름을 가리키면 OK예요.

```
FROM ./Qwen2.5-3B-Instruct.Q4_K_M.gguf
```

> 첫 줄이 다르게 되어 있으면 위 한 줄로 바꾸고 저장(`Ctrl + S`)해요.
> 둘째 줄부터(TEMPLATE, PARAMETER 등)는 **건드리지 마세요.** 대화 형식 설정이에요.

**2. 터미널에서 등록하기**

```powershell
cd lead_model_gguf
ollama create mbcsports -f Modelfile
```

`success`가 나오면 끝 ✅ (1~2분 걸려요)

**3. 확인하기**

```powershell
ollama list
```

목록에 **두 개**가 보이면 성공 ✅

```
NAME                 SIZE
mbcsports:latest     1.9 GB    ← 내 모델
qwen2.5:3b           1.9 GB    ← 원본
```

> 🔒 `ollama create`는 **내 PC 안에만** 등록해요. 인터넷에 올라가지 않아요.
> 온라인에 올리는 명령은 `ollama push`뿐이고, **이 수업에서는 쓰지 않아요.**

---

## ⑥ 비교 — `4_compare_results.ipynb`

**1.** 첫 칸의 설정에서 내 모델 이름을 확인해요.

```python
MY_MODEL = 'mbcsports'   # ollama list 에 나온 내 모델 이름
BLIND    = False         # True: 이름을 가리고 A·B·C로 섞기 (학생 블라인드 평가용)
RERUN    = False         # True: 저장된 답을 무시하고 다시 묻기
```

**2.** 위에서부터 칸을 실행해요 (`Run All`도 돼요).

| 칸 | 결과 |
|---|---|
| 2. 세 모델 답 받기 | `answers.jsonl` 저장 (다음부터는 다시 묻지 않고 불러와요) |
| 3-1. 표로 보기 | 정답 리드와 세 모델 답 전체 |
| 3-2. 자동 체크 | 모델별 요약표 (끝인사 없음 · 2문장 이하 · 길이 · 본문에 없는 숫자) |
| 4. 웹 비교표 | `compare_report.html`이 브라우저로 열려요 |

**3.** 웹 비교표에서 리포트 본문을 펼쳐 **사실이 맞는지** 직접 대조하고, 카드 아래 체크박스에 표시해요.

> 💡 **A · B · C가 뭔가요?** `BLIND = True`일 때만 나와요. 누가 쓴 답인지 모르고 고르도록 **문제마다 순서를 새로 섞어요.**
> 그래서 1번 문제의 A와 2번 문제의 A는 다른 모델일 수 있어요. 다 고른 뒤 맨 아래 **🔑 정답지**로 확인해요.
> 평소에는 `BLIND = False`로 두면 원본(회색) → 내 모델(초록) → GPT(파랑) 순서로 고정돼요.

---

## ⑦ 날씨로 톤 시험 — `5_weather_tone_test.ipynb`

스포츠 리포트로만 배운 모델에 **한 번도 안 본 날씨**를 넣어서, MBC 리드 말투가 따라오는지 봐요.

| 부분 | 넣는 것 | 결과 파일 |
|---|---|---|
| ① 날씨 리포트 | `test_weather.jsonl` (MBC 뉴스데스크 날씨 리포트 5건, 이 폴더에 넣기) | `weather_report.html` |
| ② 날씨 데이터 | Open-Meteo 내일 예보 숫자 (서울·강릉·대전·부산·제주, 가입 필요 없음) | `meteo_report.html` |

첫 칸의 `MY_MODEL`만 확인하고 위에서부터 실행하면 돼요. ②는 정답이 없으니 **메모에 없는 숫자를 지어내지 않았는지**를 가장 먼저 보세요.

---

## Ollama 명령어 한눈에

| 명령 | 하는 일 |
|---|---|
| `ollama list` | 내 PC에 있는 모델 목록 |
| `ollama ps` | 지금 GPU에 올라와 있는 모델 |
| `ollama run mbcsports` | 내 모델과 직접 대화 (끝내기: `/bye`) |
| `ollama stop mbcsports` | GPU에서 내리기 (지워지지는 않아요) |
| `ollama rm mbcsports` | 내 모델 지우기 (다시 등록하고 싶을 때) |

---

## 막혔을 때

| 이런 메시지가 나오면 | 이렇게 해요 |
|---|---|
| `'ollama' 용어가 … 인식되지 않습니다` | ④ 스크립트 실행. 그래도 안 되면 VS Code를 껐다 켜기 |
| `SyntaxError` (Jupyter 칸에 ollama 명령) | 터미널에서 실행하기. Jupyter 칸에서는 앞에 `!` 붙이기 |
| `NameError` | Jupyter 노트북 맨 위 「▶ 환경 준비」 칸부터 다시 실행 |
| `(실패: APIConnectionError)` | 시작 메뉴에서 Ollama 실행 → `ollama list` |
| `(실패: BadRequestError)` | ⑤ 등록을 안 했거나, 코드가 아직 `'내모델이름'` |
| `ollama create`에서 파일을 못 찾음 | `cd lead_model_gguf`를 했는지, Modelfile 첫 줄 이름이 맞는지 확인 |

---

## ⚠ 꼭 지킬 것

- **`2_train_unsloth_gpu.ipynb`의 `%pip install unsloth` 칸은 실행하지 마세요.**
  GPU를 못 쓰게 될 수 있어요. (`torch.cuda.is_available()`가 `False`가 됨)
  이미 실행했다면 Jupyter 칸에서 아래를 실행하고 **Restart** 하세요.
  ```python
  %pip install --force-reinstall --no-deps torch==2.11.0 torchvision --index-url https://download.pytorch.org/whl/cu128
  ```
- **학습하는 동안에는 비교 칸을 실행하지 마세요.** GPU 메모리가 부족해져요.

---

## GitHub에 올리지 않는 것

아래는 `.gitignore`로 막혀 있어요. **직접 `git add` 하지 마세요.**

| 종류 | 파일 | 이유 |
|---|---|---|
| 데이터 | `*.csv` `*.jsonl` `answers_*.json` `*_report.html` | MBC 기사 내용 (내부 학습용) |
| 모델 | `lead_model*/` `*.gguf` `outputs/` `unsloth_compiled_cache/` | 용량이 크고, 공개하지 않아요 |
| 키 | `.env` | OpenAI API 키 |

> Jupyter 노트북을 커밋할 때는 먼저 **Clear All Outputs**(모든 출력 지우기) → 저장.
> 출력 칸에 기사 본문과 모델 답이 남아 있어요.
