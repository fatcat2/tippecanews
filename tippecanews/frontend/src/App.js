import React from 'react';
import './App.css';
import { PageHeader, Row, Col, Alert } from 'antd';
import { Typography, Divider, List } from 'antd';
const { Title, Paragraph } = Typography;

const use_list = [
  "Getting Purdue News Slack releases in #tippecanews",
  "Getting CMS, TCMS and TownNews email links",
  "Searching the Purdue Directory",
  "Getting bylines"
]

const get_list = [
  "/cms - Gives the link to CMS (the online system, can use from anywhere)",
  "/tcms - Gives the link to TCMS (the local print system, can only use on Newsroom wifi or on the Macs",
  "/email - Gives the link to the email because let's be real - who can remember it lol"
]

class App extends React.Component {
  state = {
    current: 'docs',
  };

  handleClick = e => {
    console.log('click ', e);
    this.setState({
      current: e.key,
    });
  };

  

  render() {
    return (
      <div>
        <PageHeader
          style={{
            border: '1px solid rgb(235, 237, 240)',
          }}
          title="Tippecanews"
          subTitle="HOW TO USE MY BABY"
        />
        <br />
        
        <div>
          <Row>
            <Col span={12} offset={6}>
              <Typography>
                <Title>Welcome to Tippecanews</Title>
                <Paragraph>
                  You're here because you want to unlock the full potential of my baby, Tippecanews.
                </Paragraph>
                <Divider />
                <Title level={3}>
                  What does Tippecanews do?
                </Title>
                <Paragraph>
                  Well that's a very good question! Tippecanews originally started as a Slack app to get the latest press releases,
                  but its evolved into something a bit more. With Tippecanews, you can search the Purdue Directory, get bylines, get 
                  the CMS links and more! Here's a full list of functionalities:
                </Paragraph>
                <List
                  size="large"
                  dataSource={use_list}
                  renderItem={item => <List.Item>{item}</List.Item>}
                />
                <br />
                <Paragraph>
                  Let's jump into how to make the most out of this wonderful program!
                </Paragraph>
                <Title level={3}>
                  #tippecanews
                </Title>
                <Paragraph>
                  Tippecanews, as its original intended purpose, is basically an RSS bot for Slack. So here there's not much to do except
                  watch. Well, what data does Tippecanews spit into the channel? We've got your press releases and PNG data thus far.
                  We used to have tweets, but it took up way too much space in the channel. 
                </Paragraph>
                <Title level={3}>
                  Daily coronavirus counts and inspirational quotes!
                </Title>
                <Paragraph>
                  This is a new feature that I implemented. Every day at 9 a.m. EST, Tippecanews sends a coronavirus count for Tippecanoe 
                  county straight from the ISDH, along with a random inspirational quote!
                </Paragraph>
                <Title level={3}>
                  Getting links!
                </Title>
                <Paragraph>
                  Type in the following slash commands to get the listed results.
                  <List
                  size="large"
                  dataSource={get_list}
                  renderItem={item => <List.Item>{item}</List.Item>}
                />
                </Paragraph>
                <Title level={3}>
                  Search through the directory!
                </Title>
                <Paragraph code={true}>
                  /directory [ name ]
                </Paragraph>
                <Paragraph code={true}>
                 /directory ryan chen
                </Paragraph>
                <Paragraph>
                  One new feature that I've added in is directory search. While the Purdue Directory is pretty accessible online,
                  wouldn't it be awesome to search in the directory from the comfort of Slack??? Type in /directory and the name
                  of the person you're searching for and get a list of results.
                </Paragraph>
                <Alert message="Note: if you search for a common name like 'Joe,' it will come up as having no results. Please be specific." type="warning" />
                <Title level={3}>
                  Get the bylines!!!
                </Title>
                <Paragraph>
                  Maybe you're lazy. Maybe you're pressed for time. Either way, you need your bylines done now and fast. So what do you do?
                  You type in /bylines into any Slack channel to get a message only you can see with all the bylines from the current pay period.
                  Something to note is that if it's the 17th or 2nd of the month and no articles have been posted, it will show up as no articles
                  for the pay period because there are no articles lulzzzz
                </Paragraph>
                <Divider />
                <Paragraph>
                  Tippecanews is maintained by <a href="twitter.com/ryanjengchen">@ryanjengchen</a>. Find him on Twitter, or email him at <a href="mailto:ryanjchen2@gmail.com">ryanjchen2@gmail.com</a> if you have any questions.
                </Paragraph>
                <Divider />
                <Paragraph>
                  <a href="https://slack.com/oauth/v2/authorize?user_scope=identity.basic&client_id=566562418550.1308594106323&redirect_uri=http://localhost:8080/stats"><img alt="Sign in with Slack" height="40" width="172" src="https://platform.slack-edge.com/img/sign_in_with_slack.png" srcset="https://platform.slack-edge.com/img/sign_in_with_slack.png 1x, https://platform.slack-edge.com/img/sign_in_with_slack@2x.png 2x" /></a>
                </Paragraph>
              </Typography>
            </Col>
          </Row>
        </div>
      </div>
    );
  }
}

export default App;
