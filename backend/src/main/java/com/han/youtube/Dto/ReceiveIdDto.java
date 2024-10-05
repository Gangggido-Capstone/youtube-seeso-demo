package com.han.youtube.Dto;

import com.han.youtube.Domain.ReceiveId;
import lombok.Getter;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@Getter
public class ReceiveIdDto {
    private String videoId;


    public ReceiveId toEntity(String videoId){
        return ReceiveId.builder()
                .videoId(videoId)
                .build();
    }
}
