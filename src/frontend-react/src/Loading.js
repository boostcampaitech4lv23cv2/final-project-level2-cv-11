import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Typography } from "antd";
import Editor from "./Editor";
import { GlobalContext } from "./GlobalContext";

const { Title } = Typography;

const Loading = () => {
  const navigate = useNavigate();
  const { step, setStep } = useContext(GlobalContext);
  useEffect(() => {
    if (step === 0) setStep(1);
    if (step === 3) {
      navigate("/result");
      setStep(0);
    }
  }, [step]);
  return (
    <div>
      <Title className="text-center">처리중...</Title>
      <Editor />
    </div>
  );
};

export default Loading;
