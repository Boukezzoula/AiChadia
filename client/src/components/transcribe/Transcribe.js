import * as React from 'react';
import { useState } from 'react';
import { json } from 'react-router-dom'
import Box from '@mui/joy/Box';
import Textarea from '@mui/joy/Textarea';
import Header from "../Header/Header";
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import { getAuthToken } from '../../util/auth';
import LoadingButton from '@mui/lab/LoadingButton';

export default function Transcribe() {
    const [formData, setFormData] = useState({});
    const [transcription, setTranscription] = useState("");
    const [loading, setLoading] = useState(false);
    const [isTranscribed, setToTranscribed] = useState();
    const handleTranslate = async (event) => {
        setToTranscribed(false);
        setLoading(true);
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const token = getAuthToken();

        console.log({
            url: data.get('video_url'),
            token: token

        });
        //const response = await fetch('https://mocking-bird-rest-api.onrender.com/transcriptions', {        
        const response = await fetch('http://127.0.0.1:5000/transcriptions', {
            method: 'POST',
            mode: "cors",

            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData),
        }
        )


        if (response.status === 401 || response.status === 422) {
            return response.text;
        }
        if (!response.ok) {
            throw json({ message: 'could not authenticate user' }, { status: 500 });
        } else {
            console.log("great job");
        }
        const resData = await response.json().then(
            data => {
                console.log(data)
                const result = data[0]['script']
                setTranscription(result);
                setToTranscribed(true);
                setLoading(false);
                console.log(result)
            }
        );
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value });
    }


    return (
        <div>
            <Header />
            <Box
                display={"flex"}
                sx={{
                    py: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 2,
                    alignItems: 'center',
                    alignContent: 'center',
                    alignSelf: 'center',
                    justifyContent: 'center',
                    flexWrap: 'wrap',
                    flexFlow: 'row nowrap',
                    justifySelf: 'center',
                }}

            >
                <form

                    onSubmit={handleTranslate}
                >
                    <br></br>
                    <br></br>
                    <Textarea
                        placeholder="Paste Youtube Url Here !"
                        required
                        fullWidth
                        id="video_url"
                        label="Video_url"
                        name="video_url"
                        sx={{ mb: 1 }}
                        onChange={handleChange}
                        style={{
                            width: "400px",
                            padding: "15px",
                            borderRadius: "5px",
                            outline: "none",
                            resize: "none"
                        }}
                    />
                    <br></br>
                    <Box textAlign='center'>
                        <LoadingButton
                            loading={loading}
                            loadingIndicator="Loading…"
                            variant="contained"
                            type="submit"
                        ><span>Submit</span> </LoadingButton>
                        <br></br>
                    </Box>

                </form>
            </Box>
            <Box mr={3} p={3}>
                {isTranscribed &&
                    <FormControl fullWidth sx={{ m: 2 }} variant="standard">
                        <InputLabel htmlFor="outlined-adornment-amount" > Result</InputLabel>
                        <OutlinedInput
                            multiline
                            rows={20}
                            id="outlined-adornment-amount"
                            label="result"
                            value={transcription}
                        />
                    </FormControl>
                }
            </Box>
        </div>
    )

}