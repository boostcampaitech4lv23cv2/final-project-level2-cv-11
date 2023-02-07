import { Typography, Upload, Button, Row, Col, message } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import DemoButton from "./components/DemoButton";
import LayerUpload from "./components/LayerUpload";
import Sample from "./components/Sample";

const { Title, Text } = Typography;

const Demo = () => {
  return (
    <div className="mt-4 mx-24 text-center">
      <Title>사진 업로드</Title>
      <Title level={5}>번역하고 싶은 만화 파일을 업로드 해주세요.</Title>

      <div className="flex justify-center">
        <LayerUpload title="배경 레이어" name="background" />
        <LayerUpload title="대사 레이어" name="typical" />
        <LayerUpload title="효과음 레이어" name="untypical" />
      </div>

      <DemoButton />
      <div className="my-8 border-b" />

      <Title level={5}>사진이 없다면 샘플 이미지로 체험해보세요.</Title>
      <div className="flex justify-center">
        <Sample title="샘플 1" name="sample1" />
        <Sample title="샘플 2" name="sample2" />
        <Sample title="샘플 3" name="sample3" />
        <Sample title="샘플 4" name="sample4" />
      </div>
    </div>
  );
};

export default Demo;
