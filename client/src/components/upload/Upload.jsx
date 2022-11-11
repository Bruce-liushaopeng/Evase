import React from 'react'

import Icon from '@mdi/react'
import {
    mdiArchiveCancelOutline,
    mdiCloudUploadOutline,
    mdiFileChartCheckOutline,
    mdiDotsVertical,
    mdiFileChartOutline
} from '@mdi/js'

import { 
    Card,
    Divider,
    CardHeader,
    CardAction,
    CardMedia,
    CardContent,
    IconButton,
    Subtitle2,
    H6,
    Body2,
    withResize
} from 'ui-neumorphism'
import { DropzoneDialog } from "material-ui-dropzone"


class UploadForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedFile: null,
            fileSelected: false,
            fileUploaded: false,
            dialogOpen: false
        }
    }

    cancelFile = (e) => {
        this.props.onCancel()
        this.setState({
            selectedFile: null,
            fileSelected: false,
            fileUploaded: false
        });
        e.preventDefault();
        console.log("File upload cancelled, state reset.")
    }

    handleUpload = (e) => {
        e.preventDefault();
        let result = this.props.onUpload(this.state.selectedFile);
        console.log(result);
        this.setState({ 
            fileUploaded: result
        })
    }

    showDialog = () => {
        this.setState({dialogOpen: true});
    }

    handleDialogSave = (files) => {
        console.log("Save called")
        this.setState({
            dialogOpen: false,
            selectedFile: files[0],
            fileSelected: true
        });
        console.log("File was selected.")
        console.log(files)
    }

    handleDialogClose = () => {
        this.setState({dialogOpen: false});
        console.log("File dialog closed.")
    }

    actionButtonHelper = () => {

        const chooseFile = (
            <IconButton
                onClick={this.showDialog}
                className='nub-1'
            >
                {this.state.fileSelected ? (
                    <Icon path={mdiFileChartCheckOutline} size={2} />
                ) : (
                    <Icon path={mdiFileChartOutline} size={2} />
                )
                }
            </IconButton>
        )
        let uploadFile = (<></>);
        let cancelFile = (<></>);

        if (this.state.fileSelected) {
            if (!this.state.fileUploaded) {
                uploadFile = (
                    <IconButton 
                        className='nub-2'
                        onClick={this.handleUpload}
                    >
                        <Icon path={mdiCloudUploadOutline} size={2}></Icon>
                    </IconButton>
                )
            }
            cancelFile = (
                <IconButton 
                    className='nub-3'
                    onClick={this.cancelFile}
                >
                    <Icon path={mdiArchiveCancelOutline} size={2}></Icon>
                </IconButton>
            )
        }
        return (
            <CardAction>
                {chooseFile}
                {uploadFile}
                {cancelFile}
            </CardAction>
        )
    }

    fileDetailsHelper = () => {

        let fileDetails = (<></>)

        if (this.state.fileSelected) {
            fileDetails = (
                <>
                    <H6>File Details</H6><br />
                    <Body2>
                        {this.state.fileUploaded ? (
                            <>An upload attempt was made.<br /><br /></>
                        ): ("")} 

                        Filename: {this.state.selectedFile.name}<br />
                        Filetype: {this.state.selectedFile.type}<br />
                        Size in bytes: {this.state.selectedFile.size}<br />
                        Date last modified:{' '}
                        {this.state.selectedFile.lastModifiedDate.toLocaleDateString()}
                    </Body2>
                </>
            )
        }
        return (
            <CardContent>
                {fileDetails}
            </CardContent>
        )
    }

    render() {
        return (
            <>
                <CardHeader 
                title={<H6>{this.props.title}</H6>}
                subtitle={<Subtitle2>{this.props.subtitle}</Subtitle2>}
                action={
                    <IconButton>
                      <Icon path={mdiDotsVertical} size={1}></Icon>
                    </IconButton>
                  }
                />
                <CardMedia dark src="./logo.png" height={500} width={700}/>
                <Divider dense />
                {this.actionButtonHelper()}
                <Divider dense />
                {this.fileDetailsHelper()}
                <DropzoneDialog
                    open={this.state.dialogOpen}
                    onSave={this.handleDialogSave}
                    showPreviews={true}
                    onClose={this.handleDialogClose}
                    submitButtonText="Confirm"
                    filesLimit={1}
                    maxFileSize={500000000}
                />
                
            </>
        )
    }
}

export default withResize(UploadForm);