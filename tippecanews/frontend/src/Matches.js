import React, { useState, useEffect } from 'react';
import { PageHeader, Row, Col, Alert, Avatar } from 'antd';
import { Typography, Divider, List } from 'antd';
import {
    useParams,
    useLocation
} from "react-router-dom";

const axios = require("axios");
const { Title, Paragraph } = Typography;


function useQuery() {
    return new URLSearchParams(useLocation().search);
}

function Match(props){
    return (
        <div>
            <Paragraph>
                <Avatar src={props.profilePicURL} /> You matched with {props.name} during the week of {props.week} 
            </Paragraph>
            <Divider />
        </div>
    )
}

export default function Matches(props){
    let query = useQuery();

    const [matches, setMatches] = useState([{name: "Adrian Gaeta", week: "Sept. 27, 2020", profilePicURL: "https://ca.slack-edge.com/T41AUJR45-UMLPDU3PU-21fc3988e900-512"}])
    
    useEffect(() => {
        axios.post("/matchdata", {
            code: query.get("code")
        })
        .then((data) => {
            setMatches(data.matches)
        })
    })

    console.log(matches)
    return (
        <div>{matches.map((value)=>{return <Match name={value.name} week={value.week} profilePicURL={value.profilePicURL} />})}</div>
    )
}