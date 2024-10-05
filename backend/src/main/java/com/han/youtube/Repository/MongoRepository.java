package com.han.youtube.Repository;

import com.han.youtube.Domain.ReceiveId;

public interface MongoRepository extends org.springframework.data.mongodb.repository.MongoRepository<ReceiveId,String> {
}
