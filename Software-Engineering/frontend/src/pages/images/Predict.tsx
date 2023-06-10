import {Button, Carousel, Form, Input, InputNumber, Layout, Menu, message, theme, Upload} from 'antd';
import ImgCrop from 'antd-img-crop';
import { PlusOutlined } from '@ant-design/icons';
import type {RcFile, UploadFile, UploadProps} from 'antd/es/upload/interface';
import React, {useState} from 'react';
import {LogoutOutlined, UploadOutlined, VideoCameraOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import {responseType, uploadType} from "../../types/users.ts";
import {upload} from "../../apis/users.ts";

const Predict: React.FC = () => {
  const {
    Content,
    Footer,
    Sider,
  } = Layout;

  const {
    token: {colorBgContainer},
  } = theme.useToken();

  const contentStyle: React.CSSProperties = {
    height: '160px',
    color: '#fff',
    lineHeight: '160px',
    textAlign: 'center',
    background: '#364d79',
  };

  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const onChange: UploadProps['onChange'] = ({ fileList: newFileList }) => {
    setFileList(newFileList);
  };

  const onPreview = async (file: UploadFile) => {
    let src = file.url as string;
    if (!src) {
      src = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(file.originFileObj as RcFile);
        reader.onload = () => resolve(reader.result as string);
      });
    }
    const image = new Image();
    image.src = src;
    const imgWindow = window.open(src);
    imgWindow?.document.write(image.outerHTML);
  };

  const [form] = Form.useForm();

  const onFinish = async (values: uploadType) => {
    console.log(values);
    // const response = await upload(values) as responseType;
    // if (response.result_code === 200) {
    //   message.success('Upload Successfully!');
    // } else {
    //   message.error('Upload Failed!');
    // }
  }

  return (
    <Layout style={{height: '100%'}}>
      <Sider>
        <div className="demo-logo-vertical"/>
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
          <Menu.Item key="logout" icon={<LogoutOutlined/>}>
            <Link to="/">Logout</Link>
          </Menu.Item>
          <Menu.Item key="upload" icon={<UploadOutlined/>}>
            <Link to="/upload">Upload</Link>
          </Menu.Item>
          <Menu.Item key="gallery" icon={<VideoCameraOutlined/>}>
            <Link to="/gallery">Gallery</Link>
          </Menu.Item>
        </Menu>
      </Sider>

      <Layout>
        <Content>
          <div style={{paddingTop: '3%', minHeight: 'calc(100vh - 100px)', background: colorBgContainer}}>
            <Carousel style={{paddingLeft: '22%', paddingRight: '22%'}} autoplay>
              <div>
                <h2 style={contentStyle}>batch_size = 32</h2>
              </div>
              <div>
                <h2 style={contentStyle}>epochs = 20</h2>
              </div>
              <div>
                <h2 style={contentStyle}>learning_rate = 0.01</h2>
              </div>
            </Carousel>

            <Form
              name="basic"
              form={form}
              labelCol={{span: 10}}
              wrapperCol={{span: 6}}
              initialValues={{remember: true}}
              onFinish={onFinish}
              autoComplete="off"
              style={{marginTop: '3%'}}
            >
              <h1 style={{textAlign: "center"}}>Upload your handwriting</h1>

              <Form.Item
                label="Label"
                name="label"
                rules={[{required: true, message: 'Input image label'}]}
              >
                <InputNumber min={0} max={9} />
              </Form.Item>

              <Form.Item
                label="Image"
                name="image"
                valuePropName="fileList"
                rules={[{required: true, message: 'Upload image'}]}
              >
                <ImgCrop rotationSlider>
                  <Upload
                    action="http://127.0.0.1:8000/api/v1/upload_server"
                    listType="picture-card"
                    fileList={fileList}
                    onChange={onChange}
                    onPreview={onPreview}
                  >
                    {fileList.length < 1 && (
                      <div>
                        <UploadOutlined />
                        <div style={{ marginTop: 8 }}>Upload</div>
                      </div>
                    )}
                  </Upload>
                </ImgCrop>
              </Form.Item>

              <Form.Item wrapperCol={{offset: 8, span: 16}}>
                <Button type="primary" htmlType="submit">
                  Submit
                </Button>
              </Form.Item>
            </Form>
          </div>
        </Content>

        <Footer style={{textAlign: 'center', height: '20px', marginBottom: '15px'}}>
          MNIST Classification ©2023 Created by Jingbo Su
        </Footer>
      </Layout>
    </Layout>
  );
};

export default Predict;
