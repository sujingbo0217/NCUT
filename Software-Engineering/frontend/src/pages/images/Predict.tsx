import React, {useState} from 'react';
import {Link} from "react-router-dom";
import {useNavigate} from "react-router-dom";

import {Button, Carousel, Form, InputNumber, Layout, Menu, message, theme, Upload} from 'antd';
import type {RcFile, UploadFile, UploadProps} from 'antd/es/upload/interface';
import {LogoutOutlined, UploadOutlined, VideoCameraOutlined} from "@ant-design/icons";
import ImgCrop from 'antd-img-crop';

import {responseType} from "../../types/images";
import {uploadImage} from "../../apis/images";

const Predict: React.FC = () => {
  const navigate = useNavigate();

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

  const [form] = Form.useForm();
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const onChange: UploadProps['onChange'] = ({fileList: newFileList}) => {
    // console.log(newFileList);
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

  const beforeUpload = (file) => {
    if (fileList.length === 0) {
      setFileList(file);
    } else {
      message.error('More than one file').then();
    }
    return false;
  }

  const onFinish = async () => {
    const label = form.getFieldValue('label');
    const image = fileList[0];

    const data = new FormData();
    data.append('label', String(label));
    data.append('image', image.originFileObj);

    // console.log({
    //   label: String(label),
    //   image: image.originFileObj,
    // });

    try {
      const response = await uploadImage(data) as responseType;
      if (response.result_code === 201) {
        navigate('/gallery');
        message.success('Upload Successfully!');
      } else {
        message.error('Upload Failed!');
      }
    } catch (err) {
      console.log(err);
    }
  }

  const onReset = () => {
    form.resetFields();
    setFileList([]);
  };

  const buttonLayout = {
    wrapperCol: {offset: 6},
    style: {marginTop: '2.5%'},
  };

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
              wrapperCol={{span: 4}}
              initialValues={{remember: true}}
              onFinish={onFinish}
              autoComplete="off"
              style={{marginTop: '2%'}}
            >
              <h1 style={{textAlign: "center"}}>Upload your handwriting</h1>

              <Form.Item
                label="Label"
                name="label"
                rules={[{required: true, message: 'Input image label'}]}
              >
                <InputNumber min={0} max={9}/>
              </Form.Item>

              <div style={{marginTop: '3%', marginLeft: '0.6%'}}>
                <ImgCrop rotationSlider>
                  <Upload
                    listType="picture-card"
                    fileList={fileList}
                    onChange={onChange}
                    onPreview={onPreview}
                    beforeUpload={beforeUpload}
                  >
                    {fileList.length < 1 && (
                      <div>
                        <UploadOutlined/>
                        <div style={{marginTop: 6}}>Upload</div>
                      </div>
                    )}
                  </Upload>
                </ImgCrop>
              </div>

              <Form.Item {...buttonLayout}>
                <Button htmlType="button" onClick={onReset} style={{marginRight: '20px'}}>
                  Cancel
                </Button>
                <Button type="primary" htmlType='submit'>
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
