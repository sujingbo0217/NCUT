import React from "react";
import {Link, useNavigate} from "react-router-dom";

import {Button, Form, Input, Layout, Menu, message, theme} from 'antd';
import {UserOutlined} from "@ant-design/icons";
import {loginType, responseType} from "../../types/users";
import {login} from "../../apis/users.ts";

const Login: React.FC = () => {
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

  const userLogin = async (values: loginType) => {
    const response = await login(values) as responseType;
    if (response.result_code === 200) {
      message.success('Login Successfully!');
      navigate('/home');
    } else {
      message.error('Login Error!');
    }
  };

  return (
    <Layout style={{height: '100%'}}>
      <Sider collapsedWidth="0">
        <div className="demo-logo-vertical"/>
        <Menu theme="dark" mode="inline">
          <Menu.Item key="login" icon={<UserOutlined/>}>
            <Link to={'/register'}>Sign up</Link>
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
              onFinish={userLogin}
              autoComplete="off"
              style={{marginTop: '10%'}}
            >
              <h1 style={{textAlign: 'center'}}>Sign in</h1>
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

export default Login;
