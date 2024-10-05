package com.han.youtube.controller;


import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.service.DataService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:9000")
public class DataController {

    private final DataService dataService;

    @PostMapping("/api/embed-video")
    public ResponseEntity<String> recieveId(@RequestBody ReceiveIdDto videoId){
        dataService.save(videoId);
        return ResponseEntity.ok("스프링에서 비디오 ID 잘 받음"); // 이후 수정 할 예정. 당분간만 사용
    }

}
