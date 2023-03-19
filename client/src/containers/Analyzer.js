import React, {useState, useEffect, useRef} from "react";
import ReactJson from 'react-json-view';
import { Network, Options } from 'vis-network';
import PopUpCodeBlock from "./PopUpCodeBlock";

const {default: axios} = require("axios");

const Analyzer = ({ready, readyCallback, errorMsg, infoMsg}) => {

    const [analysisResult, setAnalysisResult] = useState(null);
    const [showResult, setShowResult] = useState(false);

    const visJsRef = useRef(null);

    const graph_options = {
        configure: {
            "enabled": false
        },
        nodes: {
            "shape": "dot"
        },
        edges: {
            color: {
                inherit: true
            },
            smooth: {
                enabled: true,
                type: "dynamic"
            }
        },
        interaction: {
            dragNodes: true,
            hideEdgesOnDrag: false,
            hideNodesOnDrag: false
        },
        physics: {
            enabled: true,
            stabilization: {
                enabled: true,
                fit: true,
                iterations: 1000,
                onlyDynamicEdges: false,
                updateInterval: 50
            }
        }
    };

    useEffect(() => {
        const fetchResult = async () => {
            let result = null;

            let uuid = sessionStorage.getItem('uuid');
            if (uuid) {
                const options = {
                    headers: {"content-type": "application/json"},
                    params: {"uuid": uuid}
                }

                await axios
                    .get("http://127.0.0.1:5000/analyze", options)
                    .then(function (res) {
                        const type = res.headers.get("Content-Type");
                        if (type.indexOf("application/json") !== -1) {
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
                        if (error.response) {
                            errorMsg("The server could not process your request at this time. Apologies.");
                        } else if (error.request) {
                            errorMsg("The server did not receive your request at this time. Apologies.");
                        } else {
                            errorMsg("The client could not assemble your request at this time. Apologies.");
                        }

                    });
            } else {
                errorMsg("Couldn't attempt analysis, project id not known.")
            }
        };

        if (ready) {
            fetchResult();
            console.log(analysisResult);
            console.log(showResult);
            readyCallback(analysisResult);
        }
    }, [ready])

    useEffect(() => {
        try {
            if (showResult && visJsRef && analysisResult) {
                const nodes = analysisResult['graph']['total']['nodes'];
                const edges = analysisResult['graph']['total']['edges'];

                console.log("NODES")
                console.log(nodes)
                console.log("EDGES")
                console.log(edges)

                const network = visJsRef.current && new Network(
                    visJsRef.current,
                    {
                        nodes: nodes,
                        edges: edges
                    },
                );
                network.setOptions(graph_options);
                network.on("click", function (params) {
                    if (params.nodes.length === 0 && params.edges.length > 0) {

                    } else if (params.nodes.length > 0) {

                    } else {
                        console.log("IDK");
                    }
                })
            }
        } catch (err) {
            console.log(err);
            errorMsg("There was an issue displaying the result of your analysis.");
        }
    }, [visJsRef, analysisResult])

    return (
        <div className='w-full'>
            <div>
                {showResult ? (
                    <div className="pl-4 pr-4 pb-4 pt-1 shadow-md rounded-lg">
                        <p className='font-semibold text-xl'>Analysis Result</p>
                        <div className='textcolor'>
                            <div className='h-[650px] min-w-[650px] items-stretch my-4 shadow-md rounded-lg' ref={visJsRef}></div>

                            <ReactJson className='textcolor' src={analysisResult ? analysisResult : {}} displayDataTypes={false} collapsed={1}
                                       displayObjectSize={false}/>
                        </div>
                    </div>
                ) : (
                    <></>
                )}

            </div>
        </div>
    );
}

export default Analyzer;