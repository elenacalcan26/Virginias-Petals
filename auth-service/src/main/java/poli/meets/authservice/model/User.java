package poli.meets.authservice.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name = "user_poli")
@Data
public class User implements Serializable {

    @Id
    @GeneratedValue(strategy =  GenerationType.SEQUENCE, generator = "userSequenceGenerator")
    @SequenceGenerator(
            name = "userSequenceGenerator",
            sequenceName = "user_sequence_generator",
            allocationSize = 1
    )
    @Column(name = "id")
    private Long id;

    @Column(name = "username")
    private String username;

    @Column(name = "password")
    @JsonIgnore
    private String password;
}