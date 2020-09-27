import React from 'react';
import './App.css';
import { PageHeader, Row, Col, Alert } from 'antd';
import { Typography, Divider, List } from 'antd';

import queryString from "query-string";

import Information from "./Information"
import Matches from "./Matches"


import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useParams,
  useLocation
} from "react-router-dom";

function App(){
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
              <Router>
                <Switch>
                  <Route path="/meetups">
                    <Matches />
                  </Route>
                  <Route path="/">
                    <Information />
                  </Route>
                </Switch>
              </Router>
            </Col>
          </Row>
        </div>
    </div>
  );
}

export default App;
