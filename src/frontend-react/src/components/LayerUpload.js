import { useState, useContext, useEffect } from "react";
import { Col, Typography, Upload, message } from "antd";
import styled from "styled-components";
import { GlobalContext } from "../GlobalContext";

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

// title: UI 상에 표시될 제목
// name: 전역 상태에 저장될 이름
const LayerUpload = ({ title, name }) => {
  const [imgURL, setImgURL] = useState(null);
  const { files, setFiles } = useContext(GlobalContext);
  const setFile = (name, file) => {
    setFiles({ ...files, [name]: file });
    setImgURL(URL.createObjectURL(file));
  };

  useEffect(() => {
    const file = files[name];
    if (file) {
      setImgURL(URL.createObjectURL(file));
    }
  }, [files]);

  return (
    <div className="m-2">
      <Title level={5}>{title}</Title>
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
          className="hover:opacity-50"
          style={{ backgroundImage: `url(${imgURL})` }}
        >
          +
        </Button>
      </Upload>
    </div>
  );
};

export default LayerUpload;
