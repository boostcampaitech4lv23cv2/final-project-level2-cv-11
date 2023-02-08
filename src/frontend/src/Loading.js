import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Steps } from "antd";
import Editor from "./Editor";
import { GlobalContext } from "./GlobalContext";
import { LoadingOutlined } from "@ant-design/icons";

const f = (step) => {
  if (step === 10) return 0;
  if (step === 11) return 1;
  if ((20 <= step && step <= 23) || step === 3) return 2;
  if (step === 4) return 3;
  return 0;
};

const Loading = () => {
  const navigate = useNavigate();
  const { step, setStep } = useContext(GlobalContext);
  useEffect(() => {
    window.scrollTo(0, 0);
    return () => {
      setStep(0);
    };
  }, []);
  useEffect(() => {
    if (step === 0) setStep(10);
  }, [step]);

  const stepitems = [
    { title: "OCR" },
    { title: "폰트 생성" },
    { title: "대사 생성" },
    { title: "마무리" },
  ];
  stepitems[f(step)].icon = <LoadingOutlined />;

  return (
    <div>
      <div className="w-[800px] my-10 mx-auto">
        <Steps current={f(step)} items={stepitems} />
      </div>
      <Editor auto />
    </div>
  );
};

export default Loading;
