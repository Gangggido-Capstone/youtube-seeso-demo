import React, { useState, useEffect } from "react";
import VideoList from "./VideoList";
import SearchBar from "./SearchBar";
import { fetchPopularVideos, searchVideos } from "./api/youtubeApi";
import { useNavigate } from "react-router-dom";
import "../../css/main.css";

const MainPage = () => {
    const [videos, setVideos] = useState([]);
    const [searchResults, setSearchResults] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        loadPopularVideos();
    }, []);

    const loadPopularVideos = async () => {
        try {
            const data = await fetchPopularVideos();
            setVideos(data);
        } catch (error) {
            console.error("Error loading popular videos", error);
        }
    };

    const handleSearch = async (query) => {
        try {
            const data = await searchVideos(query);
            setSearchResults(data);
        } catch (error) {
            console.error("Error during search", error);
        }
    };

    const handleSettingsClick = () => {
        navigate("/Settings");
    };
    const handleRecordClick =() => {
        navigate("/Records");
    };

    return (
        <div>
            <a href='/'>
                <img src='/eye_logo.gif' alt='Logo' className='logo' />
            </a>
            <SearchBar onSearch={handleSearch} />
            <VideoList
                videos={searchResults.length > 0 ? searchResults : videos}
            />
            <img
                src='/settings.png'
                alt='Settings Icon'
                className='settings-icon'
                onClick={handleSettingsClick}
            />
            <img
                src='/record.png'
                alt='Record Icon'
                className='record-icon'
                onClick={handleRecordClick}
            />
        </div>
    );
};

export default MainPage;
