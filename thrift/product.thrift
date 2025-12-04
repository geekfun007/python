/**
 * Product Service Thrift Definition
 * 产品服务 Thrift 定义
 */

namespace py product_service
namespace java com.example.product

/**
 * 产品信息
 */
struct Product {
    1: required i32 id,
    2: required string name,
    3: optional string description,
    4: required double price,
    5: required i32 stock,
    6: optional string category,
    7: optional i32 owner_id,
    8: required string created_at,
    9: required string updated_at
}

/**
 * 创建产品请求
 */
struct CreateProductRequest {
    1: required string name,
    2: optional string description,
    3: required double price,
    4: optional i32 stock,
    5: optional string category,
    6: optional i32 owner_id
}

/**
 * 更新产品请求
 */
struct UpdateProductRequest {
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
    2: required list<Product> items
}

/**
 * 库存更新请求
 */
struct StockUpdateRequest {
    1: required i32 quantity
}

/**
 * 统计信息
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
    2: required string message,
    3: optional string data
}

/**
 * 异常定义
 */
exception ProductNotFoundException {
    1: string message
}

exception ProductAlreadyExistsException {
    1: string message
}

exception ValidationException {
    1: string message
}

/**
 * 产品服务接口
 */
service ProductService {
    /**
     * 创建产品
     */
    Product createProduct(1: CreateProductRequest request) 
        throws (1: ProductAlreadyExistsException paee, 2: ValidationException ve),
    
    /**
     * 获取产品
     */
    Product getProduct(1: i32 product_id) 
        throws (1: ProductNotFoundException pnfe),
    
    /**
     * 获取产品列表
     */
    ProductListResponse getProductList(1: i32 skip, 2: i32 limit, 3: string category),
    
    /**
     * 更新产品
     */
    Product updateProduct(1: i32 product_id, 2: UpdateProductRequest request) 
        throws (1: ProductNotFoundException pnfe, 2: ValidationException ve),
    
    /**
     * 删除产品
     */
    Response deleteProduct(1: i32 product_id) 
        throws (1: ProductNotFoundException pnfe),
    
    /**
     * 更新库存
     */
    Product updateStock(1: i32 product_id, 2: StockUpdateRequest request) 
        throws (1: ProductNotFoundException pnfe),
    
    /**
     * 价格区间查询
     */
    ProductListResponse getProductsByPriceRange(1: double min_price, 2: double max_price, 3: i32 skip, 4: i32 limit),
    
    /**
     * 分类统计
     */
    list<CategoryStatistics> getCategoryStatistics()
}
