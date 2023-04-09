import React, {useState, useEffect, useRef, useCallback, useMemo} from "react";
import ReactJson from 'react-json-view';
import { Network } from 'vis-network';
import CodeReportBlock from "./CodeReportBlock";
import {getNodeProperties} from "./ContainerUtil";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { getLogContents, getAnalysisResult } from '../util/Hooks';
import Ping from "./Ping";

const {default: axios} = require("axios");

const Analyzer = ({ready, readyCallback, errorMsg, infoMsg, onNodeClick, dark}) => {
    // if the app is running in docker, we use the ENV defined in docker
    // otherwise the fixed port is used
    const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT || '5050'
    const BACKEND_URL = `http://localhost:${BACKEND_PORT}`

    const [analysisResult, setAnalysisResult] = useState(null);
    const [showResult, setShowResult] = useState(false);
    const [network, setNetwork] = useState(null);
    const [uuid, setUuid] = useState(null);
    const [logContents, setLogContents] = useState(null);
    const [showLog, setShowLog] = useState(false);

    const visJsRef = useRef(null);
    const vulNodesRef = useRef([]);

    const MemoCodeBlock = React.memo(CodeReportBlock);

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

    /**
     * OnClick event handler for nodes in the Network graph being clicked.
     * useCallback to update whenever the network or prop is updated.
     *
     * @param  {Object} params The object containing nodes and edges clicked
     */
    const onNetworkClick = useCallback((params) => {
        if (params.nodes.length === 0 && params.edges.length > 0) {
        } else if (params.nodes.length > 0) {
            let node_id = params.nodes[0];
            //console.log("doClick node clicked: ", node_id);
            onNodeClick(node_id);         // for some reason this needs to be awaited
        } else {
        }
    }, [onNodeClick, network]);

    useEffect(() => {

        if (network != null) {
            network.off("click");           // remove previous listener
            network.on("click", onNetworkClick);
        }

    }, [onNetworkClick, network]);


    useEffect(() => {

        // stop it from being called all the time
        if (uuid && ready() && visJsRef) {

            getAnalysisResult(uuid)
                .then(function (res) {
                    const type = res.headers.get("Content-Type");
                    if (type.indexOf("application/json") !== -1) {
                        if (res.data) {
                            setAnalysisResult(res.data);
                            setShowResult(true);
                            readyCallback(res.data);
                            infoMsg("Your vulnerabilities have been detected!");
                            setUuid(null);
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
        }
    }, [uuid]);

    // set the id to the session storage retrieval
    useEffect(() => {
        setUuid(sessionStorage.getItem('uuid'));
    }, [ready]);

    // show log contents only when set
    useEffect(() => {
        if (logContents != null) {
            setShowLog(true);
        }
    }, [logContents]);

    // draw the graph
    useEffect(() => {
        try {
            if (showResult && visJsRef && analysisResult) {

                // collect nodes and edges
                const nodes = analysisResult['graph']['total']['nodes'];
                const edges = analysisResult['graph']['total']['edges'];

                const net = visJsRef.current && new Network(
                    visJsRef.current,
                    {
                        nodes: nodes,
                        edges: edges
                    },
                );
                net.setOptions(graph_options);
                setNetwork(net);
            }
        } catch (err) {
            console.log(err);
            errorMsg("There was an issue displaying the result of your analysis.");
        }
    }, [visJsRef, analysisResult])

    useEffect(() => {
        if (analysisResult) {
            // map the current data
            vulNodesRef.current = analysisResult['graph']['total']['nodes'].filter(node => node['vulnerable'] === true).map(node => getNodeProperties(node));
        }
    }, [analysisResult]);

    /**
     * Function to generate vulnerable report blocks.
     * Memoized components to stop unnecessary refreshes.
     */
    const vulBlocks = useMemo(() => {
        if (showResult && vulNodesRef.current.length > 0) {
            return vulNodesRef.current.map((node) => (
            <MemoCodeBlock
                id={node.moduleName+":"+node.functionName}
                {...node}
                doClick={() => onNodeClick(node.moduleName+":"+node.functionName)}
            />
            ));
        }
        return [];
    }, [showResult, vulNodesRef.current, onNodeClick])

    /**
     * The current theme for the log.
     * Updates when the dark prop is changed.
     *
     * @type {Object}
     */
    const logTheme = useMemo(() => {
        if (dark) {
          return vscDarkPlus;
        } else {
          return vs;
        }
        }, [dark]);

    /**
     * Log file display elements.
     * Only refreshes when contents of log or general theme is changed.
     */
    const logDisplay = useMemo(() => {
        if (logContents != null) {
            return (
                <div className='w-full'>
                    <SyntaxHighlighter className='rounded-xl md:max-h-[400px] lg:max-h-[600px]' wrapLines={true} style={logTheme}>
                        {logContents}
                    </SyntaxHighlighter>
                </div>
            )
        }
    }, [logContents, logTheme]);


    // function used to get the contents of the log from the backend
    /**
     * Function to request log contents from the backend.
     * Throws errors
     */
    const getLogContentsSub = useCallback(() => {

        getLogContents(uuid)
            .then(response => setLogContents(response.data))
            .catch(function (error) {
                if (error.response) {
                    errorMsg("The server could not process your request at this time. Apologies.");
                } else if (error.request) {
                    errorMsg("The server did not receive your request at this time. Apologies.");
                } else {
                    errorMsg("The client could not assemble your request at this time. Apologies.");
                }
            })

    }, [uuid, setLogContents]);


    /**
     * The current theme for the JSON display.
     * Changes when the dark prop is set.
     *
     * @type {Object}
     */
    const myTheme = useMemo(() => {
        if (dark) {
            return 'codeschool';
        } else {
            return 'rjv-default';
        }
    }, [dark]);

    // style for the JSON view
    const styler = {
        width: '100%',
        padding: '10px',
        'border-radius': '0.75rem'
    };

    return (
        <div className='w-full'>
            <div>
                {showResult ? (
                    <div className="pl-4 pr-4 pb-4 pt-1 shadow-md rounded-lg">
                        <p className='font-semibold text-4xl'>Analysis Result</p>
                        <div className='flex flex-row w-full'>
                            <div className='w-1/3 flex flex-col mr-4'>
                                {vulBlocks}
                            </div>
                            <div className='textcolor w-2/3'>
                                <div className='h-[650px] items-stretch my-4 shadow-md rounded-lg' ref={visJsRef}></div>
                                <button className="rounded-md drop-shadow-md hover:drop-shadow-lg mr-10 my-4 color2" onClick={getLogContentsSub}>
                                    <Ping></Ping>
                                    <p className="px-4 py-1">Show Log</p>
                                </button>
                                {
                                    (showLog) ? (
                                        logDisplay
                                    ): (<></>)
                                }
                                <div className="w">
                                    <ReactJson className='color-1' src={analysisResult ? analysisResult['graph'] : {}} displayDataTypes={true} collapsed={1}
                                           displayObjectSize={false} enableClipboard={false} name="graph" theme={myTheme} style={styler}/>
                                </div>
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