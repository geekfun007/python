/**
 * User Service Thrift IDL
 * 用户服务 Thrift 接口定义
 */

namespace py user_service
namespace java com.example.user

/**
 * 用户基本信息
 */
struct UserInfo {
    1: required i32 id,
    2: required string username,
    3: required string email,
    4: optional string full_name,
    5: optional i32 age,
    6: optional bool is_active = true,
}

/**
 * 创建用户请求
 */
struct CreateUserRequest {
    1: required string username,
    2: required string email,
    3: required string password,
    4: optional string full_name,
    5: optional i32 age,
}

/**
 * 用户列表响应
 */
struct UserListResponse {
    1: required list<UserInfo> users,
    2: required i32 total,
}

/**
 * 通用响应
 */
struct Response {
    1: required i32 code,
    2: required string message,
    3: optional string data,
}

/**
 * 用户服务异常
 */
exception UserServiceException {
    1: required i32 code,
    2: required string message,
}

/**
 * 用户服务接口
 */
service UserService {
    /**
     * 创建用户
     */
    UserInfo createUser(1: CreateUserRequest request) throws (1: UserServiceException error),
    
    /**
     * 获取用户信息
     */
    UserInfo getUser(1: i32 user_id) throws (1: UserServiceException error),
    
    /**
     * 获取用户列表
     */
    UserListResponse listUsers(1: i32 skip, 2: i32 limit) throws (1: UserServiceException error),
    
    /**
     * 更新用户
     */
    UserInfo updateUser(1: i32 user_id, 2: map<string, string> updates) throws (1: UserServiceException error),
    
    /**
     * 删除用户
     */
    Response deleteUser(1: i32 user_id) throws (1: UserServiceException error),
}
