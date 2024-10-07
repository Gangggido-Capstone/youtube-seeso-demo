package com.han.youtube.controller;


import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.service.DataService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
public class TestController {

    private final DataService dataService;

    @GetMapping("/test/idlist")
    public ResponseEntity<List> idList(){
        List<ReceiveIdDto> idList = dataService.findId();
        System.out.println("id리스트");
        System.out.println(idList);
        return ResponseEntity.ok(idList);
    }
}
