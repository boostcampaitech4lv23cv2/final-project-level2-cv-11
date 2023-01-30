import { useState, useContext, useEffect } from "react";
import { Col, Typography, Upload, message } from "antd";
import styled from "styled-components";
import { FileContext } from "../FileContext";

const { Title } = Typography;

const Button = styled.button`
  width: 300px;
  height: 300px;
  border: 1px solid #d9d9d9;
  text-align: center;
  vertical-align: middle;
  font-size: 50px;
  background-color: transparent;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  &:hover {
    cursor: pointer;
  }
`;

const LayerUpload = ({ name }) => {
  const [imgURL, setImgURL] = useState(null);
  const { files, setFiles } = useContext(FileContext);
  const setFile = (name, file) => {
    files[name] = file;
    setFiles(files);
    setImgURL(URL.createObjectURL(file));
  };

  useEffect(() => {
    const file = files[name];
    if (file) {
      setImgURL(URL.createObjectURL(file));
    }
  }, [files]);

  return (
    <Col span={8}>
      <div style={{ textAlign: "center" }}>
        <Title level={5}>{name}</Title>
        <Upload
          name="file"
          accept="image/*"
          maxCount={1}
          onChange={(info) => {
            if (info.file.status !== "uploading") {
            }
            if (info.file.status === "done") {
              message.success(`${info.file.name} file uploaded successfully`);
            } else if (info.file.status === "error") {
              message.error(`${info.file.name} file upload failed.`);
              console.log("error", info);
            }
          }}
          customRequest={({ file, onSuccess }) => {
            setFile(name, file);
            onSuccess();
          }}
        >
          <Button
            style={{
              backgroundImage: `url(${imgURL})`,
            }}
          >
            +
          </Button>
        </Upload>
      </div>
    </Col>
  );
};

export default LayerUpload;
