package com.characters.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbBean;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbAttribute;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@DynamoDbBean
public class CurrentStatus {
    private Integer hp;
    private Integer maxHp;
    private String condition;
    private List<String> buffs;
    
    @DynamoDbAttribute("max_hp")
    public Integer getMaxHp() {
        return maxHp;
    }
    
    public void setMaxHp(Integer maxHp) {
        this.maxHp = maxHp;
    }
}
