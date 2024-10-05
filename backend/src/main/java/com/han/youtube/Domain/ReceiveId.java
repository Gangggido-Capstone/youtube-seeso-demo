package com.han.youtube.Domain;


import jakarta.persistence.Id;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "Capstone")
@Getter
@NoArgsConstructor
public class ReceiveId {
    @Id
    private String id;
    private String videoId;

    @Builder
    public ReceiveId(String videoId){
        this.videoId = videoId;
    }
}
