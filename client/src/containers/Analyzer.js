import React, {useState, useEffect, useRef} from "react";
import ReactJson from 'react-json-view';
import { Network, Options } from 'vis-network';
import PopUpCodeBlock from "./PopUpCodeBlock";
import CodeReportBlock from "./CodeReportBlock";

const {default: axios} = require("axios");

const Analyzer = ({ready, readyCallback, errorMsg, infoMsg, onNodeClick}) => {

    const [analysisResult, setAnalysisResult] = useState(null);
    const [showResult, setShowResult] = useState(false);
    const [uuid, setUuid] = useState(null);

    const visJsRef = useRef(null);

    const doClick = (node)=>{onNodeClick(node)};

    const graph_options = {
        configure: {
            "enabled": false
        },
        nodes: {
            "shape": "dot"
        },
        edges: {
            color: {
                inherit: false,
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

            if (uuid && ready) {
                await axios
                    .post("http://127.0.0.1:5000/analyze", {
                        'uuid': uuid,
                    }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(function (res) {
                        const type = res.headers.get("Content-Type");
                        if (type.indexOf("application/json") !== -1) {
                            if (res.data) {
                                result = res.data;
                                setAnalysisResult(result);
                                setShowResult(true);
                                console.log("callback");
                                readyCallback(result);
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

        // stop it from being called all the time
        if (uuid && ready && visJsRef) {
            fetchResult();
        }
    }, [uuid])

    // set the id to the session storage retrieval
    useEffect(() => {
        setUuid(sessionStorage.getItem('uuid'));
    }, [ready])

    // draw the graph
    useEffect(() => {
        try {
            if (showResult && visJsRef && analysisResult) {

                // collect nodes and edges
                const nodes = analysisResult['graph']['total']['nodes'];
                const edges = analysisResult['graph']['total']['edges'];

                // set up network in vis js
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
                        console.log(params.nodes[0]);
                        doClick(params.nodes[0]);
                    } else {
                    }
                })
            }
        } catch (err) {
            console.log(err);
            errorMsg("There was an issue displaying the result of your analysis.");
        }
    }, [visJsRef, analysisResult])

    // make the vulnerable report blocks
    const makeVulBlocks = () => {
        if (analysisResult && showResult) {

            const nodes = analysisResult['graph']['total']['nodes'];

            // collect vulnerable nodes
            let vul_nodes = nodes.filter((node) => node['vulnerable']===true);

            return Object.keys(vul_nodes).map((key) => {
                let spl = vul_nodes[key]['id'].replace(":", ".").split(".");
                let fn = spl.pop();
                spl = spl.join(".");
                return (
                    <CodeReportBlock doClick={()=>doClick(vul_nodes[key].id)} moduleName={spl} startLine={1} endLine={1} functionName={fn} />
                )
            })
        }
    }

    return (
        <div className='w-full'>
            <div>
                {showResult ? (
                    <div className="pl-4 pr-4 pb-4 pt-1 shadow-md rounded-lg">
                        <p className='font-semibold text-4xl'>Analysis Result</p>
                        <div className='flex flex-row w-full'>
                            <div className='w-1/3 flex flex-col mr-4'>
                                {makeVulBlocks()}
                            </div>
                            <div className='textcolor w-2/3'>
                                <div className='h-[650px] items-stretch my-4 shadow-md rounded-lg' ref={visJsRef}></div>
                                <ReactJson className='textcolor' src={analysisResult ? analysisResult : {}} displayDataTypes={false} collapsed={1}
                                           displayObjectSize={false}/>
                            </div>
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