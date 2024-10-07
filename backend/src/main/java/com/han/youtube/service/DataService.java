package com.han.youtube.service;

import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.ReceiveIdDto;

import java.util.List;

public interface DataService {
    void save(ReceiveIdDto receiveIdDto);

    List<ReceiveIdDto> findId();
}
