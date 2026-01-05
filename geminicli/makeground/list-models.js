const { GoogleGenerativeAI } = require("@google/generative-ai");

// 환경변수에 등록한 API 키를 사용합니다.
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

async function listModels() {
  try {
    // 사용 가능한 모델 목록을 가져오는 메서드입니다.
    const models = await genAI.listModels();
    
    console.log("=== [사용 가능한 Gemini 모델 리스트] ===");
    console.log(JSON.stringify(models, null, 2)); // JSON 형식으로 예쁘게 출력
    
    console.log("\n💡 팁: 위 리스트에서 'name' 부분에 있는 값을 복사해서 index.js의 model 설정에 넣으세요.");
  } catch (error) {
    console.error("모델 리스트를 가져오는 중 오류 발생:", error);
  }
}

listModels();