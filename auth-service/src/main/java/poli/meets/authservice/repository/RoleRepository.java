package poli.meets.authservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import poli.meets.authservice.model.Role;
import poli.meets.authservice.model.UserRole;

import java.util.List;

@Repository
public interface RoleRepository extends JpaRepository<Role, Long> {

    @Query("select ur.role from UserRole ur, User u where u.id = ur.user.id and u.username like :username")
    List<Role> findRolesByUsername(String username);
}
