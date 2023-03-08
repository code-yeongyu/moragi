# 모락이 🍚

모락이는 [CJ 프레시밀](https://front.cjfreshmeal.co.kr/)에서 오늘의 식단 정보를 가져와 슬랙 웹훅을 통해 전송하는 기능을 제공합니다. ✨

본 프로젝트에 설정된 [깃허브 액션](https://github.com/code-yeongyu/moragi/blob/master/.github/workflows/daily_job.yml)의 cron schedule 설정에 따라 평일 한국시간 9시마다 되고있어요. 따라서, 별도의 서버 없이 작동하고 있는 중입니다!

현재는 [무신사](https://musinsa.com)의 구내식당인 '모락모락'의 식단 정보를 가져오고 있습니다. 🍚

## 사용법 📖

### 사전 준비물 🔨

1. 슬랙 워크스페이스
1. 슬랙 웹훅 URL
    1. 없다면 생성해주세요! 구글에 좋은 가이드가 많습니다.
1. *CJ 프레시밀을 사용하는 구내식당*
    - 안타깝게도 이건 구글링 하셔도 생성이 불가능합니다 !

### 시작 🚀

아래 이미지 처럼 `Use this template` -> `Create a new repository` 를 통해 본 저장소를 복제합니다.
![clone](https://raw.githubusercontent.com/code-yeongyu/moragi/master/images/clone.png)

복제한 저장소의 `Settings` -> `Secrets` 에서 `SLACK_WEBHOOK_URL` 에 슬랙 웹훅 URL 을 추가해주세요! 그렇다면 아래와 같을것입니다.

![secrets](https://raw.githubusercontent.com/code-yeongyu/moragi/master/images/actions-secrets.png)

이제는 지금 회사의 식당 정보를 등록해야 하는데요! curl 와 jq 를 이용해서 `CJ_FRESH_MEAL_STORE_ID` 를 알아내야 합니다. 없다면 미리 설치해주시고, 다음의 명령어를 입력해주세요!

```sh
curl 'https://front.cjfreshmeal.co.kr/store/v1/search-store?page=1&schKey=%EB%AC%B4%EC%8B%A0%EC%82%AC&isList=false' | jq '.data.storeList[0].idx'
```

그러면 아래 사진과 같이, 결과값이 나옵니다. 이 중 숫자값만 복사해주세요.

![store_id](https://raw.githubusercontent.com/code-yeongyu/moragi/master/images/store-id.png)

이번에는 `Settings` -> `Variables` 에서 `CJ_FRESH_MEAL_STORE_ID` 에 해당 값을 추가해주세요!

![variables](https://raw.githubusercontent.com/code-yeongyu/moragi/master/images/actions-variables.png)

이제 모두 설정이 끝났습니다! 이제 아래 사진처럼 `Actions` -> `일해라 모락이` -> `Run workflow` 을 통해 실행해보세요! 혹은 설정된 cron schedule 에 따라 자동으로 실행됩니다. 기본값은 평일 9시입니다!

![work-moragi](https://raw.githubusercontent.com/code-yeongyu/moragi/master/images/work-moragi.png)

이제 밥 먹으러 가볼까요!! 😋
