import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainPage from "./MainPage";
import VideoGazeTracker from "./VideoGazeTracker";
import InitSeeso from "./InitSeeso";
import VideoPlayer from "./VideoPlayer";

const EyeTrackingApp = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<MainPage />} />
                <Route
                    path='/play-video/:videoId'
                    element={<VideoGazeTracker />}
                />
                <Route path='/seeso' element={<InitSeeso />} />
                <Route path='/youtube' element={<VideoGazeTracker />} />
                <Route path='/Video' element={<VideoPlayer />} />
            </Routes>
        </BrowserRouter>
    );
};

export default EyeTrackingApp;
