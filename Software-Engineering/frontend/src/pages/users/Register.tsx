import React from "react";
import {Link, useNavigate} from "react-router-dom";

import {Button, Form, Input, Layout, Menu, message, theme} from 'antd';
import {LoginOutlined} from "@ant-design/icons";
import {registerType, responseType} from "../../types/users";
import {register} from "../../apis/users.ts";


const Register: React.FC = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const {
    Content,
    Footer,
    Sider,
  } = Layout;

  const {
    token: {colorBgContainer},
  } = theme.useToken();

  const userRegister = async (values: registerType) => {
    const {username, password, confirm} = values;
    if (password !== confirm) {
      message.error('Twice Different Password!');
      return;
    }
    if (password.length < 8 || password.length > 16) {
      message.error('Password should be 8 to 16 characters!');
      return;
    }
    const response = await register({username, password}) as responseType;
    // Register -> Login
    if (response.result_code === 201) {
      message.success('Register Successfully!');
      navigate('/');
    } else {
      message.error('Username Exists!');
    }
  };

  return (
    <Layout style={{height: '100%'}}>
      <Sider collapsedWidth="0">
        <div className="demo-logo-vertical"/>
        <Menu theme="dark" mode="inline">
          <Menu.Item key="register" icon={<LoginOutlined/>}>
            <Link to={'/'}>Sign in</Link>
          </Menu.Item>
        </Menu>
      </Sider>

      <Layout>
        <Content>
          <div style={{
            padding: 24,
            minHeight: 'calc(100vh - 100px)',
            background: colorBgContainer,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
          }}>
            <Form
              name="basic"
              form={form}
              labelCol={{span: 8}}
              wrapperCol={{span: 16}}
              initialValues={{remember: true}}
              onFinish={userRegister}
              autoComplete="off"
              style={{marginTop: '10%'}}
            >
              <h1 style={{textAlign: 'center'}}>Sign up</h1>
              <Form.Item
                label="Username"
                name="username"
                rules={[{required: true, message: 'Please input your username'}]}
              >
                <Input/>
              </Form.Item>

              <Form.Item
                label="Password"
                name="password"
                rules={[{required: true, message: 'Please input your password'}]}
              >
                <Input.Password/>
              </Form.Item>

              <Form.Item
                label="Confirm"
                name="confirm"
                rules={[{required: true, message: 'Confirm your password'}]}
              >
                <Input.Password/>
              </Form.Item>

              <Form.Item wrapperCol={{offset: 18, span: 16}}>
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

export default Register;
