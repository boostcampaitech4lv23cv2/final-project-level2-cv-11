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
    if (step === 0) setStep(1);
    if (step === 4) {
      navigate("/result");
      setStep(0);
    }
    if (step === -1) {
      message.error("OCR 도중 에러가 발생했습니다.\n다시 시도해주세요.");
      navigate("/demo");
      setStep(0);
    }
  }, [step]);
  const msg = [
    "에러",
    "대사 인식중...",
    "번역 중...",
    "번역 중...",
    "마무리 중...",
    "결과 페이지로 이동...",
  ][step];
  return (
    <div>
      <Title className="text-center">{msg}</Title>
      <Editor />
    </div>
  );
};

export default Loading;
