import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Typography } from "antd";
import Editor from "./Editor";
import { FileContext } from "./FileContext";

const { Title } = Typography;

const Loading = () => {
  const navigate = useNavigate();
  const { step, setStep } = useContext(FileContext);
  useEffect(() => {
    if (step === 0) setStep(1);
    if (step === 3) {
      navigate("/result");
      setStep(0);
    }
  }, [step]);
  return (
    <div>
      <Title style={{ textAlign: "center" }}>처리중...</Title>
      <Editor />
    </div>
  );
};

export default Loading;
