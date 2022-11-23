import { useState, useEffect } from 'react'

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

function UploadFileForm(props) {

    const [selectedFile, setSelectedFile] = useState(null);
    const [fileUploaded, setFileUploaded] = useState(false);
    const [uploadAttempt, setUploadAttempt] = useState(0);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [currentMessage, setCurrentMessage] = useState("");
    const [responseMessage, setResponseMessage] = useState("");

    const removeFile = () => {
        console.log("EvaseUploader: Cancel function triggered.")
        const resultOfRemoval = props.doRemove();
        setFileUploaded(false);
        setSelectedFile(null);
        setUploadAttempt(0);
    }

    const uploadFile = (file) => {
        console.log("EvaseUploader: Upload function triggered.")
        const resultOfUpload = props.doUpload(file);
        if (resultOfUpload) {
            setFileUploaded(true);
        }
        setUploadAttempt(uploadAttempt+1);
    }

    const showDialog = () => {
        setDialogOpen(true);
    }

    const handleDialogSave = (files) => {
        console.log("Save called");
        setDialogOpen(false);
        setSelectedFile(files[0]);
        
        console.log("File was selected.");
        console.log(files);
    }

    const handleDialogClose = () => {
        setDialogOpen(false);
        console.log("File dialog closed.");
    }

    const actionButtonHelper = () => {

        const chooseFileBtn = (
            <IconButton
                rounded
                text={false}
                onClick={showDialog}
                className='nub-1'
                
            >
                {selectedFile ? (
                    <Icon path={mdiFileChartCheckOutline} size={2} />
                ) : (
                    <Icon path={mdiFileChartOutline} size={2} />
                )
                }
            </IconButton>
        )
        let uploadFileBtn = (<></>);
        let cancelFileBtn = (<></>);

        if (selectedFile) {
            if (!fileUploaded) {
                uploadFileBtn = (
                    <IconButton 
                        rounded
                        text={false}
                        className='nub-2'
                        onClick={uploadFile}
                        
                    >
                        <Icon path={mdiCloudUploadOutline} size={2}></Icon>
                    </IconButton>
                )
            }
            cancelFileBtn = (
                <IconButton
                    rounded
                    text={false}
                    className='nub-3'
                    onClick={removeFile}
                    
                >
                    <Icon path={mdiArchiveCancelOutline} size={2}></Icon>
                </IconButton>
            )
        }
        return (
            <CardContent >
                {chooseFileBtn}
                {uploadFileBtn}
                {cancelFileBtn}
            </CardContent>
        )
    }

    const fileDetailsHelper = () => {

        let fileDetails = (<></>)

        if (selectedFile) {
            fileDetails = (
                <>
                    <H6 >File Details</H6><br />
                    <Body2 >
                        {uploadAttempt>0 ? (
                            <>An upload attempt was made.<br /><br /></>
                        ): ("")} 

                        Filename: {selectedFile.name}<br />
                        Filetype: {selectedFile.type}<br />
                        Size in bytes: {selectedFile.size}<br />
                        Date last modified:{' '}
                        {selectedFile.lastModifiedDate.toLocaleDateString()}
                    </Body2>
                </>
            )
        }
        return (
            <CardContent >
                {fileDetails}
            </CardContent>
        )
    }

    return (
        <>
        <CardHeader 
        title={<H6 >{props.title}</H6>}
        subtitle={<Subtitle2 >{props.subtitle}</Subtitle2>}
        action={
            <IconButton >
                <Icon path={mdiDotsVertical} size={1}></Icon>
            </IconButton>
            }
        
        />
        {props.useIcon ? (<CardMedia src={props.iconpath} height={500} width={700} />):(<></>)}
        
        <Divider dense  />
        {actionButtonHelper()}
        <Divider dense  />
        <CardContent >
            <Body2 >
                Upload attempts: {uploadAttempt}
            </Body2>
        </CardContent>
        {fileDetailsHelper()}
        <DropzoneDialog
            open={dialogOpen}
            onSave={handleDialogSave}
            showPreviews={true}
            onClose={handleDialogClose}
            submitButtonText="Confirm"
            filesLimit={1}
            maxFileSize={500000000}
        />
        <CardContent >
            <>
            <Body2 >
                {currentMessage}
            </Body2>

            {uploadAttempt>0 ? (
                <>
                    <H6 >Response Message</H6>
                    <Body2 >
                        {responseMessage}
                    </Body2>
                </>
                ) :
                (
                    <></>
                )}
            </>
        </CardContent>
    </>
    );
}

function defaultDoRemove() {
    return true;
}

function defaultDoUpload() {
    return true;
}

UploadFileForm.defaultProps = {
    title: "Upload Form",
    subtitle: "Please upload your file below",
    doRemove: (defaultDoRemove),
    doUpload: (defaultDoUpload),
    useIcon: false,
    dark: false
}

export default UploadFileForm;