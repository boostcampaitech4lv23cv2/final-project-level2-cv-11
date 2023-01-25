import { useEffect, useState } from "react";
import { UploadOutlined } from "@ant-design/icons";
import { Button, message, Upload, Col, Divider, Row } from "antd";
import { Typography } from "antd";
import { fabric } from "fabric";
import Editor from "./Editor";
const { Title } = Typography;

const props = {
  name: "file",
  accept: "image/*",
  maxCount: 1,
  onChange(info) {
    if (info.file.status !== "uploading") {
      console.log(info.file, info.fileList);
    }
    if (info.file.status === "done") {
      message.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === "error") {
      message.error(`${info.file.name} file upload failed.`);
      console.log("error", info);
    }
  },
};

const App = () => {
  const [back, setBack] = useState(null);
  const [typical, setTypical] = useState(null);
  const [typicalFile, setTypicalFile] = useState(null);

  const makeCustomRequest = (set, setFile = null) => {
    return ({ file, onSuccess }) => {
      if (setFile) setFile(file);
      const reader = new FileReader();
      reader.onload = (event) => {
        const imgObj = new Image();
        imgObj.src = event.target.result;
        imgObj.onload = () => {
          const image = new fabric.Image(imgObj);
          set(image);
        };
      };
      reader.readAsDataURL(file);
      onSuccess();
    };
  };

  const fetchAndSet = (path, set, setFile = null) => {
    fetch(path)
      .then((res) => res.blob())
      .then((blob) => {
        if (setFile) setFile(blob);
        const reader = new FileReader();
        reader.onload = (event) => {
          const imgObj = new Image();
          imgObj.src = event.target.result;
          imgObj.onload = () => {
            const image = new fabric.Image(imgObj);
            set(image);
          };
        };
        reader.readAsDataURL(blob);
      });
  };

  useEffect(() => {
    fetchAndSet("./background.png", setBack);
    fetchAndSet("./typical.png", setTypical, setTypicalFile);
  }, []);

  return (
    <div
      style={{
        margin: "0 auto",
        textAlign: "center",
      }}
    >
      <Title>웹툰 번역</Title>

      <Divider>업로드</Divider>
      <Row justify="center">
        <Col span={4}>
          <Upload
            customRequest={makeCustomRequest(setBack)}
            defaultFileList={[
              {
                uid: "1",
                name: "background.png",
                url: "./background.png",
              },
            ]}
            {...props}
          >
            <Button icon={<UploadOutlined />}>배경 업로드</Button>
          </Upload>
        </Col>
        <Col span={4}>
          <Upload
            customRequest={makeCustomRequest(setTypical, setTypicalFile)}
            defaultFileList={[
              {
                uid: "1",
                name: "typical.png",
                url: "./typical.png",
              },
            ]}
            {...props}
          >
            <Button icon={<UploadOutlined />}>대사 업로드</Button>
          </Upload>
        </Col>
        <Col span={4}>
          <Upload {...props}>
            <Button icon={<UploadOutlined />}>효과음 업로드(미구현)</Button>
          </Upload>
        </Col>
      </Row>

      <Divider>편집</Divider>

      <div style={{ border: "1px solid" }}>
        <Editor background={back} typical={typical} typicalFile={typicalFile} />
      </div>
    </div>
  );
};

export default App;
