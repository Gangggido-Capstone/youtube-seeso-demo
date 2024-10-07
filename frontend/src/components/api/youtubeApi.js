import axios from "axios";

const API_BASE_URL = "http://localhost:8080/api";

export const fetchPopularVideos = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/popular-videos`);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error fetching popular videos", error);
        throw error;
    }
};

export const searchVideos = async (query) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/search-videos`, {
            params: { query },
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error searching videos", error);
        throw error;
    }
};
export const embedVideo = async (videoId) => {
    try {
        // 영상 ID를 백엔드로 전송
        const response = await axios.post(`${API_BASE_URL}/embed-video`, { videoId });
        console.log("Response from backend:", response.data); // 응답 확인
        return response.data;
    } catch (error) {
        console.error("Error embedding video", error);
        throw error;
    }
};


