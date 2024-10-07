package com.han.youtube.service.Impl;

import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.Repository.MongoRepository;
import com.han.youtube.service.DataService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class DataServiceImpl implements DataService {

    private final MongoRepository mongoRepository;

    @Transactional
    @Override
    public void save(ReceiveIdDto receiveIdDto){
        ReceiveId receiveId = receiveIdDto.toEntity(receiveIdDto.getVideoId());
        mongoRepository.save(receiveId);
    }

    @Transactional
    @Override
    public List<ReceiveIdDto>findId(){
        return mongoRepository.findBy(PageRequest.of(0,10));
    }
}
