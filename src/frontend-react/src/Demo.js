import { useState, useContext, useEffect } from "react";
import { Typography, Upload, Button, Row, Col, message } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { FileContext } from "./FileContext";
import DemoButton from "./components/DemoButton";
import LayerUpload from "./components/LayerUpload";

const { Title, Text } = Typography;

const B = styled.button`
  width: 160px;
  height: 80px;
  border-radius: 20px;
  border: none;
  margin-top: 20px;
  background: deepskyblue;
  font-size: 22px;
  font-weight: bold;
  color: white;
  &:hover {
    cursor: pointer;
  }
`;

const Sample = () => {
  const { setFiles } = useContext(FileContext);
  return (
    <div
      style={{
        width: "300px",
        height: "300px",
        textAlign: "center",
      }}
    >
      <Title level={5}>샘플 1</Title>
      <img
        src="/background.png"
        style={{
          border: "1px solid #d9d9d9",
          width: "100%",
          height: "100%",
        }}
      />
      <Button
        onClick={async () => {
          console.log("click");

          const names = ["background", "typical", "untypical"];

          const blobs = await Promise.all(
            names.map((name) => fetch(`/${name}.png`).then((res) => res.blob()))
          );

          const files = {
            background: blobs[0],
            typical: blobs[1],
            untypical: blobs[2],
          };

          setFiles(files);
          console.log("files", files);
        }}
      >
        선택
      </Button>
    </div>
  );
};

const Demo = () => {
  const navigate = useNavigate();
  return (
    <div style={{ margin: "0 100px 100px" }}>
      <Title>사진 업로드</Title>
      <Title level={5}>번역하고 싶은 만화 파일을 업로드 해주세요.</Title>

      <Row justify={"center"} gutter={1}>
        <LayerUpload name="background" />
        <LayerUpload name="typical" />
        <LayerUpload name="untypical" />
      </Row>

      <div style={{ height: "50px" }} />

      <DemoButton />

      <Title level={5}>사진이 없다면 데모 이미지로 체험해보세요.</Title>
      <Text>데모 이미지 선택 버튼 추가 예정</Text>
      <Sample />
    </div>
  );
};

export default Demo;
