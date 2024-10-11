package com.han.youtube.controller;

import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.service.GazeDataService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api")
public class GazeDataController {

    private final GazeDataService gazeDataService;

    @PostMapping("/save-gaze-data")
    public ResponseEntity<String> saveGazeData(@RequestBody Map<String, Object> payload) {
        try {
            gazeDataService.saveGazeData(payload);
            return new ResponseEntity<>("CSV 파일 및 db저장이 성공적으로 저장되었습니다.", HttpStatus.OK);
        } catch (Exception e) {
            e.printStackTrace();
            return new ResponseEntity<>("CSV 파일 및 db저장 중 오류가 발생했습니다.", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/list")
    public ResponseEntity<List<ReceiveIdDto>> dbList(){
        List<ReceiveIdDto> dbData = gazeDataService.dbData();
        return ResponseEntity.ok(dbData);
    }

}