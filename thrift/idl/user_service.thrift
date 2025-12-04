/**
 * User Service Thrift IDL
 * 用户服务 Thrift 接口定义语言
 */

namespace py user_service
namespace java com.example.user

// 用户结构体
struct User {
    1: required i32 id,
    2: required string username,
    3: required string email,
    4: optional string full_name,
    5: optional i32 age,
    6: optional bool is_active = true,
    7: optional bool is_superuser = false,
    8: optional string created_at,
    9: optional string updated_at
}

// 创建用户请求
struct CreateUserRequest {
    1: required string username,
    2: required string email,
    3: required string password,
    4: optional string full_name,
    5: optional i32 age
}

// 更新用户请求
struct UpdateUserRequest {
    1: optional string full_name,
    2: optional i32 age,
    3: optional bool is_active,
    4: optional string password
}

// 用户列表响应
struct UserListResponse {
    1: required i32 total,
    2: required list<User> items
}

// 通用响应
struct Response {
    1: required i32 code,
    2: required string message,
    3: optional string data
}

// 用户不存在异常
exception UserNotFoundException {
    1: string message
}

// 用户已存在异常
exception UserAlreadyExistsException {
    1: string message
}

// 无效参数异常
exception InvalidParameterException {
    1: string message
}

/**
 * 用户服务接口
 */
service UserService {
    /**
     * 创建用户
     */
    User createUser(1: CreateUserRequest request) 
        throws (1: UserAlreadyExistsException e1, 2: InvalidParameterException e2),
    
    /**
     * 获取用户
     */
    User getUser(1: i32 user_id) 
        throws (1: UserNotFoundException e),
    
    /**
     * 获取用户列表
     */
    UserListResponse listUsers(1: i32 skip, 2: i32 limit),
    
    /**
     * 更新用户
     */
    User updateUser(1: i32 user_id, 2: UpdateUserRequest request) 
        throws (1: UserNotFoundException e1, 2: InvalidParameterException e2),
    
    /**
     * 删除用户
     */
    Response deleteUser(1: i32 user_id) 
        throws (1: UserNotFoundException e),
    
    /**
     * 根据用户名搜索
     */
    UserListResponse searchByUsername(1: string username, 2: i32 skip, 3: i32 limit)
}
