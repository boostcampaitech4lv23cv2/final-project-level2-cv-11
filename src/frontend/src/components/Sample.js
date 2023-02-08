import { useContext } from "react";
import { Typography } from "antd";
import { GlobalContext } from "../GlobalContext";

const { Title } = Typography;

const Sample = ({ title, name }) => {
  const { setFiles } = useContext(GlobalContext);

  const handleClick = async () => {
    console.log("click");
    const names = ["background", "typical", "untypical"];
    const blobs = await Promise.all(
      names.map((x) => fetch(`/${name}/${x}.png`).then((res) => res.blob()))
    );
    const files = {
      background: blobs[0],
      typical: blobs[1],
      untypical: blobs[2],
    };
    setFiles(files);
    console.log("files", files);
  };

  return (
    <div className="w-72 m-2">
      <Title level={5}>{title}</Title>

      <div className="group relative cursor-pointer" onClick={handleClick}>
        <img
          alt="샘플 이미지"
          src={`/${name}/origin.png`}
          className="w-full h-full border group-hover:border-slate-400 group-hover:opacity-50"
        />
      </div>
    </div>
  );
};

export default Sample;
