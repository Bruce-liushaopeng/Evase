import React, {useState, useEffect} from "react";
import ReactJson from 'react-json-view';
import Graph from 'vis-react';

const {default: axios} = require("axios");

const Analyzer = ({ready, readyCallback, errorMsg, infoMsg}) => {

    const [analysisResult, setAnalysisResult] = useState({});
    const [showResult, setShowResult] = useState(false);


    useEffect(() => {
        const fetchResult = async () => {
            let result = null;

            const options = {
                headers: {"content-type": "application/json"}
            }

            await axios
                .get("http://127.0.0.1:5000/analyze", options)
                .then(function (res) {
                    const type = res.headers.get("Content-Type");
                    console.log(type);
                    console.log(res.status);
                    if (type.indexOf("application/json") !== -1) {
                        console.log("HERE");
                        console.log(res);
                        if (res.data) {
                            result = res.data;
                            setAnalysisResult(result);
                            setShowResult(true);
                            infoMsg("Your vulnerabilities have been detected!");
                        }
                    } else {
                        errorMsg("The server response could not be parsed. Apologies.");
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    if (error.response) {

                        errorMsg("The server could not process your request at this time. Apologies.");
                    } else if (error.request) {
                        errorMsg("The server did not receive your request at this time. Apologies.");
                    } else {
                        errorMsg("The client could not assemble your request at this time. Apologies.");
                    }

                });

        };


        if (ready) {
            fetchResult();
            console.log(analysisResult);
            console.log(showResult);
            readyCallback();
        }
    }, [ready])


    const events = {
        select: function(event) {
            var { nodes, edges } = event;
        }
    };

    const prettyResult = () => {
        try {
            console.log(showResult);
            console.log(analysisResult);
            if (showResult && analysisResult) {
                if (Object.keys(analysisResult).length > 0) {
                    let graph = {
                        nodes: analysisResult['graph']['total']['nodes'],
                        edges: analysisResult['graph']['total']['edges']
                    };
                    console.log("printing graph");
                    console.log(graph)

                    let options = {
                        "configure": {
                            "enabled": false
                        },
                        "nodes": {
                            "shape": "dot"
                        },
                        "edges": {
                            "color": {
                                "inherit": true
                            },
                            "smooth": {
                                "enabled": true,
                                "type": "dynamic"
                            }
                        },
                        "interaction": {
                            "dragNodes": true,
                            "hideEdgesOnDrag": false,
                            "hideNodesOnDrag": false
                        },
                        "physics": {
                            "enabled": true,
                            "stabilization": {
                                "enabled": true,
                                "fit": true,
                                "iterations": 1000,
                                "onlyDynamicEdges": false,
                                "updateInterval": 50
                            }
                        }
                    };
                    let st = {
                        width: '650px',
                        height: '650px'
                    }

                    return (
                        <div className='textcolor'>
                            <div className='min-h-[650px] w-full items-stretch'>
                                <Graph
                                    className='h-full w-full'
                                    graph={graph}
                                    style={st}
                                    options={options}
                                    events={events}
                                />
                            </div>

                            <ReactJson className='textcolor' src={analysisResult} displayDataTypes={false} collapsed={1}
                                       displayObjectSize={false}/>
                        </div>
                    );
                } else {
                    return <></>
                }
            }
        } catch (err) {
            console.log(err);
            errorMsg("There was an unexpected error when trying to display the analysis result.");
        }
    }

    return (
        <div className='w-full'>
            <div>
                {showResult ? (
                    <div className="pl-4 pr-4 pb-4 shadow-md">
                        <p className='font-semibold text-xl'>Analysis Result</p>
                        {prettyResult()}
                    </div>
                ) : (
                    <></>
                )}

            </div>
        </div>
    );
}

export default Analyzer;