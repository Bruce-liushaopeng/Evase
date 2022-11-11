import React from 'react'

import EvaseUploader from '../upload/EvaseUploader'
import EvaseAnalyzer from '../analysis/EvaseAnalyzer'
import EvaseCredits from '../credits/EvaseCredits';

import {
    H4,
    H6,
    Tab,
    Card,
    Tabs,
    Divider,
    TabItem,
    TabItems,
    ProgressLinear
  } from 'ui-neumorphism'



class HomeForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            active: 0,
            uploadComplete: false,
            analysisComplete: false
        }
    }

    progress = () => {
        return ((this.state.active+1)/2) * 100;
    }


    render() {
        const { active } = this.state

        const tabItems = (
            <TabItems value={active} >
              <TabItem>
                <div>
                <EvaseUploader />
                </div>
              </TabItem>
              <TabItem>
                <div>
                <EvaseAnalyzer />
                </div>
              </TabItem>
            </TabItems>
        );
        return (
            //<Card height={1000} width={700}>
            //<ProgressLinear
            //    value={this.progress()}
            //    color="blue"
            ///>
            //<Tabs
            //    value={active}
            //    onChange={({ active }) => this.setState({ active })}
            //>
            //    <Tab>Upload</Tab>
            //    <Tab>Analyze</Tab>
            //</Tabs>
            //{tabItems}
            //</Card>

            <Card width={700}>
                <EvaseUploader></EvaseUploader>
                <EvaseAnalyzer></EvaseAnalyzer>
                <EvaseCredits></EvaseCredits>
            </Card>
        );
    }
}

export default HomeForm;