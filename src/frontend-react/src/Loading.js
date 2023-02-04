import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Typography, message } from "antd";
import Editor from "./Editor";
import { GlobalContext } from "./GlobalContext";

const { Title } = Typography;

const Loading = () => {
  const navigate = useNavigate();
  const { step, setStep } = useContext(GlobalContext);
  useEffect(() => {
    if (step === 0) setStep(10);
  }, [step]);
  const msg = {
    0: "에러",
    10: "대사 인식중...",
    11: "폰트 생성중...",
    20: "번역 중...",
    21: "번역 중...",
    22: "번역 중...",
    3: "번역 중...",
    4: "마무리 중...",
    5: "결과 페이지로 이동...",
  }[step.toString()];
  return (
    <div>
      <Title className="text-center">{msg}</Title>
      <Editor auto />
    </div>
  );
};

export default Loading;
