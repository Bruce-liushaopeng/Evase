import AnalysisForm from './AnalysisForm'
import { analyzeCode } from './AnalysisHooks'
import React, {useState} from "react";
import ReactJson from 'react-json-view';
import Graph from 'vis-react';

const Analyzer = (props) => {

    const [analysisResult, setAnalysisResult] = useState({});

    const getAnalysisResult = async () => {
        const res = await analyzeCode();
        console.log(res);
        setAnalysisResult(res);
    }

    const events = {
        select: function(event) {
            var { nodes, edges } = event;
        }
    };

    const prettyResult = () => {
        console.log("analysis Result");
        console.log(analysisResult)
        if (Object.keys(analysisResult).length > 0) {
            console.log("PRETTY")
            console.log(analysisResult);
    
            
                let graph = {
                    nodes: analysisResult['graph']['total']['nodes'],
                    edges: analysisResult['graph']['total']['edges']
                };
                console.log("printing graph");
                console.log(graph)
    
                var options = {
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
                return (
                    <div>
                        <div className='h-96'>
                            <Graph
                            graph={graph}
                            options={options}
                            events={events}
                        />
                        </div>
    
                        <ReactJson src={analysisResult} displayDataTypes={false} collapsed={1} displayObjectSize={false}/>
                    </div>
                );
        } else {
            return <></>
        }
        



        //return (<pre>{JSON.stringify(analysisResult, null, 2)}</pre>);
    }

    return (
      <AnalysisForm onSubmission={getAnalysisResult} analysisResult={prettyResult()}/>
    );
}

export default Analyzer;