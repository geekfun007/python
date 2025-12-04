/**
 * Product Service Thrift IDL
 * 产品服务 Thrift 接口定义
 */

namespace py product_service
namespace java com.example.productservice

/**
 * 产品结构体
 */
struct Product {
    1: required i32 id,
    2: required string name,
    3: optional string description,
    4: required double price,
    5: required i32 stock,
    6: optional string category,
    7: optional i32 owner_id,
    8: optional i64 created_at,
    9: optional i64 updated_at
}

/**
 * 产品创建请求
 */
struct ProductCreateRequest {
    1: required string name,
    2: optional string description,
    3: required double price,
    4: optional i32 stock,
    5: optional string category,
    6: optional i32 owner_id
}

/**
 * 产品更新请求
 */
struct ProductUpdateRequest {
    1: optional string name,
    2: optional string description,
    3: optional double price,
    4: optional i32 stock,
    5: optional string category
}

/**
 * 产品列表响应
 */
struct ProductListResponse {
    1: required i32 total,
    2: required list<Product> products
}

/**
 * 库存更新请求
 */
struct StockUpdateRequest {
    1: required i32 quantity
}

/**
 * 分类统计
 */
struct CategoryStatistics {
    1: required string category,
    2: required i32 count,
    3: required double avg_price,
    4: required i32 total_stock
}

/**
 * 通用响应
 */
struct Response {
    1: required i32 code,
    2: required string message
}

/**
 * 产品服务异常
 */
exception ProductNotFoundException {
    1: string message
}

exception ProductAlreadyExistsException {
    1: string message
}

exception ValidationException {
    1: string message,
    2: map<string, string> errors
}

/**
 * 产品服务接口
 */
service ProductService {
    /**
     * 创建产品
     */
    Product createProduct(1: ProductCreateRequest request) 
        throws (1: ProductAlreadyExistsException e1, 2: ValidationException e2),
    
    /**
     * 获取产品详情
     */
    Product getProduct(1: i32 product_id) 
        throws (1: ProductNotFoundException e),
    
    /**
     * 获取产品列表
     */
    ProductListResponse listProducts(1: i32 skip, 2: i32 limit, 3: optional string category),
    
    /**
     * 更新产品
     */
    Product updateProduct(1: i32 product_id, 2: ProductUpdateRequest request) 
        throws (1: ProductNotFoundException e1, 2: ValidationException e2),
    
    /**
     * 删除产品
     */
    Response deleteProduct(1: i32 product_id) 
        throws (1: ProductNotFoundException e),
    
    /**
     * 搜索产品
     */
    ProductListResponse searchProducts(1: string keyword, 2: i32 skip, 3: i32 limit),
    
    /**
     * 价格区间查询
     */
    ProductListResponse getProductsByPriceRange(1: double min_price, 2: double max_price, 3: i32 skip, 4: i32 limit),
    
    /**
     * 更新库存
     */
    Product updateStock(1: i32 product_id, 2: StockUpdateRequest request) 
        throws (1: ProductNotFoundException e),
    
    /**
     * 分类统计
     */
    list<CategoryStatistics> getCategoryStatistics()
}
